# automation_AI


```bash
+------------------------------------------------------------------------------------------------+
|                                     Network Automation Flow                                    |
+------------------------------------------------------------------------------------------------+

     User Input (Natural Language)
            |
            v
+---------------------------+
|    "Configure interface   |
| GigabitEthernet1 with IP |
|    192.168.1.1/24"       |
+---------------------------+
            |
            v
+---------------------------+        +----------------------------------------+
|    LangChain/GPT 3.5     | -----> |            Command Classifier          |
|    Natural Language      |        |                                        |
|      Processing          |        |  Analyzes intent and generates         |
+---------------------------+        |  appropriate command sets              |
                                    +----------------------------------------+
                                                     |
                    +--------------------------------+--------------------------------+
                    |                                |                                |
                    v                                v                                v
        +-----------------+                +-----------------+                +-----------------+
        |  Show Commands  |                |Config Commands  |                |Verify Commands |
        +-----------------+                +-----------------+                +-----------------+
        |                 |                |                 |                |                 |
        | • Pre-checks    |                | • Device config |                | • Post-checks   |
        | • Status views  |                | • Changes       |                | • Validation    |
        | • Diagnostics   |                | • Updates       |                | • Confirmation  |
        +-----------------+                +-----------------+                +-----------------+
                    |                                |                                |
                    v                                v                                v
        +-----------------+                +-----------------+                +-----------------+
        | Example:        |                | Example:        |                | Example:        |
        | show ip int     |                | interface Gi1   |                | show run int    |
        | brief           |                | ip address      |                | Gi1             |
        |                 |                | 192.168.1.1/24  |                | ping            |
        +-----------------+                +-----------------+                +-----------------+
                    |                                |                                |
                    +--------------------------------+--------------------------------+
                                                     |
                                                     v
                                    +----------------------------------------+
                                    |           Netmiko Executor             |
                                    |                                        |
                                    | • Connects to device                   |
                                    | • Executes commands in order          |
                                    | • Collects results                     |
                                    +----------------------------------------+
                                                     |
                                                     v
                                    +----------------------------------------+
                                    |           Results Processing           |
                                    |                                        |
                                    | • Formats output                       |
                                    | • Validates results                    |
                                    | • Generates reports                    |
                                    +----------------------------------------+
                                                     |
                                                     v
                                    +----------------------------------------+
                                    |          Streamlit Frontend            |
                                    |                                        |
                                    | • Displays results                     |
                                    | • Shows command output                 |
                                    | • Highlights status                    |
                                    +----------------------------------------+

```
# 🌟 Network Automation With AI

This project is designed to harness the power of AI for automating network operations on Cisco IOS XE devices. It translates natural language queries into precise network commands, ensuring safe execution with built-in verification and error handling.

## Key Features
- **Natural Language Processing (NLP) for Network Commands**: Translate user queries into executable network commands using AI.
- **Real-Time Command Execution and Verification**: Executes network commands instantly and verifies their accuracy before applying them.
- **Comprehensive Logging and Error Handling**: Automatically logs all operations, providing extensive error handling to prevent misconfigurations.
- **User-Friendly Interface**: Designed with a Streamlit interface for ease of use by both technical and non-technical users.
- **Secure Device Connection Management**: Securely manages connections to Cisco devices, maintaining session integrity.
- **Automatic Command Validation and Verification**: Ensures commands are valid and checks results against expected network state.

## 🛠️ Technology Stack

### Core Dependencies
- **LangGraph**: Powers the orchestration of AI-driven workflows.
- **LangChain**: Integration framework for advanced AI/LLM capabilities.
- **OpenAI GPT**: Utilizes GPT models for natural language understanding and command translation.
- **Netmiko**: Provides network device automation, supporting CLI access to Cisco IOS XE.
- **Streamlit**: Simplifies the web interface for users to interact with the platform.
- **Pydantic**: Ensures data validation and reliable settings management.

## Get Started
1. Clone the repository:
```bash
   git clone <repository-url>
```
2. Install requirments
```bash
   pip install -r requirments.txt
```
3. ENV Vars set up in .env file:
```bash
     OPENAI_API_KEY=your-key
     DEVICE_TYPE=cisco_ios
     HOST=sandbox-iosxe-latest-1.cisco.com
     USERNAME=admin
     PASSWORD=C1sco12345
```
4. Export ENV Vars:
```bash
     export $(cat .env)
```
5. Run the code
```bash
     streamlit run frontend.py
```

   
