from typing import List, Dict, TypedDict, Optional
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field
from netmiko import ConnectHandler
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('network_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Graph State class
class GraphState(TypedDict):
    query: str
    commands: Dict[str, List[str]]
    execution_results: List[Dict[str, str]]
    status: str
    error_message: Optional[str]
    timestamp: str

# Command Classification Models
class CommandType(BaseModel):
    command: str
    command_type: str = Field(description="Type of command: 'show', 'config', or 'verify'")
    prerequisites: List[str] = Field(default_list=[])
    verification_commands: List[str] = Field(default_list=[])

class CommandsList(BaseModel):
    show_commands: List[str] = Field(
        description="List of show commands to execute",
        default=[],
        examples=[["show version", "show ip interface brief"]]
    )
    config_commands: List[str] = Field(
        description="List of configuration commands to execute",
        default=[],
        examples=[["interface GigabitEthernet1", "ip address 192.168.1.1 255.255.255.0", "no shutdown"]]
    )
    verify_commands: List[str] = Field(
        description="List of verification commands to run after configuration",
        default=[],
        examples=[["show running-config interface GigabitEthernet1"]]
    )

# Device configuration class
class DeviceConfig(BaseModel):
    device_type: str = "cisco_ios"
    host: str = Field(..., description="Device IP address or hostname")
    username: str = Field(..., description="Device username")
    password: str = Field(..., description="Device password")
    port: int = Field(default=22, description="SSH port")
    timeout: int = Field(default=60, description="Connection timeout in seconds")
    fast_cli: bool = Field(default=True, description="Enable fast CLI mode")
    session_log: str = Field(default="", description="Session log file path")

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

# Enhanced command classifier with improved prompt
def nl_to_commands(state: GraphState) -> GraphState:
    query = state["query"]
    system_message = """You are an expert IOS XE Network Command Generator.
    
    Analyze the natural language query and generate appropriate network commands following these rules:
    1. Show commands: Include diagnostic and verification commands (show, ping, traceroute)
    2. Config commands: Include complete configuration sequences, properly ordered
    3. Verify commands: Include verification commands to validate configurations
    
    Important rules:
    - Configuration commands must be in the correct order
    - Include all necessary sub-commands for configuration
    - Add appropriate verification commands for each configuration
    - For interface configurations, include 'no shutdown' when enabling
    - For IP configurations, include mask in the correct format
    
    Convert this query into appropriate commands:
    Query: {query}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message)
    ])
    
    try:
        chain = prompt | llm.with_structured_output(CommandsList)
        response = chain.invoke({'query': query})
        
        state["commands"] = {
            "show": response.show_commands,
            "config": response.config_commands,
            "verify": response.verify_commands
        }
        state["status"] = "commands_generated"
        logger.info(f"Commands generated successfully: {state['commands']}")
        
    except Exception as e:
        error_msg = f"Error in command generation: {str(e)}"
        state["status"] = "failed"
        state["error_message"] = error_msg
        logger.error(error_msg)
    
    return state

# Command executor 
def execute_commands(state: GraphState) -> GraphState:
    show_commands = state["commands"].get("show", [])
    config_commands = state["commands"].get("config", [])
    verify_commands = state["commands"].get("verify", [])
    
    # Device connection details
    device = DeviceConfig(
        device_type = os.getenv("DEVICE_TYPE"),
        host = os.getenv("HOST"),
        username = os.getenv("USERNAME"),
        password = os.getenv("PASSWORD"),
        session_log=f"session_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
    
    output = []
    
    try:
        with ConnectHandler(**device.dict()) as net_connect:
            # Execute show commands
            if show_commands:
                logger.info("Executing show commands")
                for command in show_commands:
                    try:
                        result = net_connect.send_command(
                            command, 
                            strip_prompt=True, 
                            strip_command=True
                        )
                        output.append({
                            "command": command,
                            "output": result,
                            "type": "show",
                            "status": "success"
                        })
                        logger.info(f"Successfully executed show command: {command}")
                    except Exception as e:
                        error_msg = f"Error executing show command '{command}': {str(e)}"
                        output.append({
                            "command": command,
                            "output": error_msg,
                            "type": "show",
                            "status": "failed"
                        })
                        logger.error(error_msg)
            
            # Execute configuration commands
            if config_commands:
                logger.info("Executing configuration commands")
                try:
                    # Enter configuration mode and send commands
                    config_output = net_connect.send_config_set(
                        config_commands,
                        enter_config_mode=True,
                        exit_config_mode=True,
                        strip_prompt=True,
                        strip_command=True
                    )
                    
                    output.append({
                        "command": "Configuration Commands",
                        "output": config_output,
                        "type": "config",
                        "commands_executed": config_commands,
                        "status": "success"
                    })
                    logger.info("Configuration commands executed successfully")
                    
                    # Save configuration
                    save_output = net_connect.save_config()
                    output.append({
                        "command": "write memory",
                        "output": save_output,
                        "type": "config_save",
                        "status": "success"
                    })
                    logger.info("Configuration saved successfully")
                    
                except Exception as e:
                    error_msg = f"Error during configuration: {str(e)}"
                    output.append({
                        "command": "Configuration Commands",
                        "output": error_msg,
                        "type": "config",
                        "commands_attempted": config_commands,
                        "status": "failed"
                    })
                    logger.error(error_msg)
            
            # Execute verification commands
            if verify_commands:
                logger.info("Executing verification commands")
                for command in verify_commands:
                    try:
                        result = net_connect.send_command(
                            command,
                            strip_prompt=True,
                            strip_command=True
                        )
                        output.append({
                            "command": command,
                            "output": result,
                            "type": "verify",
                            "status": "success"
                        })
                        logger.info(f"Successfully executed verification command: {command}")
                    except Exception as e:
                        error_msg = f"Error executing verification command '{command}': {str(e)}"
                        output.append({
                            "command": command,
                            "output": error_msg,
                            "type": "verify",
                            "status": "failed"
                        })
                        logger.error(error_msg)
        
        state["execution_results"] = output
        state["status"] = "success"
        

        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        state["status"] = "failed"
        state["error_message"] = error_msg
        logger.error(error_msg)
    
    state["timestamp"] = datetime.now().isoformat()
    return state

# Create the workflow graph
def create_network_flow() -> StateGraph:
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("parse_commands", nl_to_commands)
    workflow.add_node("execute_commands", execute_commands)
    
    # Define edges
    workflow.add_edge("parse_commands", "execute_commands")
    
    # Set entry point
    workflow.set_entry_point("parse_commands")
    
    return workflow.compile()

