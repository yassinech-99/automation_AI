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
