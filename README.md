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
# Network Automation with AI

## Project Description
This project leverages AI to automate network operations on Cisco IOS XE devices. It translates natural language queries into precise network commands, ensuring safe execution with built-in verification and error handling. By combining AI-driven NLP and network automation frameworks, this tool enhances operational efficiency, minimizes errors, and simplifies network management for engineers and administrators.

## Business Use Case
Managing network devices through CLI-based commands can be complex and error-prone, requiring domain expertise. This solution enables users to interact with network devices using natural language, reducing the technical barrier and improving accuracy through automated validation. The project helps in:
- Automating configuration tasks
- Running diagnostics and troubleshooting commands
- Ensuring compliance with pre- and post-execution checks

## Technology Stack
- **LangGraph** - AI-driven workflow orchestration
- **LangChain** - NLP framework for AI integration
- **OpenAI GPT** - Natural language processing and command translation
- **Netmiko** - Network device automation via CLI access
- **Streamlit** - Web interface for user interactions
- **Pydantic** - Data validation and settings management

## Status
- **Version**: Beta
- **Current Progress**: Functional prototype with core automation features
- **Planned Enhancements**:
  - Support for multi-vendor environments
  - Integration with network monitoring tools

## Installation
### Prerequisites
- Python 3.8+
- Virtual Environment setup
- API key for OpenAI (GPT integration)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project folder:
   ```bash
   cd automation_AI
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set environment variables in `.env`:
   ```bash
   OPENAI_API_KEY=your-key
   DEVICE_TYPE=cisco_ios
   HOST=sandbox-iosxe-latest-1.cisco.com
   USERNAME=admin
   PASSWORD=C1sco12345
   ```
5. Export environment variables:
   ```bash
   export $(cat .env)
   ```
6. Run the application:
   ```bash
   streamlit run frontend.py
   ```

## Usage
### Example Command Flow
1. **User Input**: "Configure interface GigabitEthernet1 with IP 192.168.1.1/24"
2. **AI Processing**: LangChain interprets input and categorizes it
3. **Command Execution**:
   - Pre-checks (show commands)
   - Configuration (apply settings)
   - Verification (validate changes)
4. **Output**:
   - Display results in Streamlit UI
   - Log execution details
## Demo
[Watch the demo](demo.webm)
## Known Issues
- Limited to Cisco IOS XE devices
- Requires stable API access for AI-driven command translation
- May require additional security configurations for production use

## Getting Help
For issues, open a ticket in the repository's issue tracker.

## Contributing
- Contributions are welcome! Follow standard GitHub practices for pull requests.
- Check the [CONTRIBUTING](CONTRIBUTING.md) file for details.

## License
This code is licensed under the BSD 3-Clause License. See [LICENSE](LICENSE) for details.

## Related Resources
- Cisco DevNet Sandbox: [Multi-IOS Cisco Test Network](https://devnetsandbox.cisco.com/RM/Topology)
- Learning Labs: [Model Driven Programmability (NETCONF/YANG)](https://developer.cisco.com/)

