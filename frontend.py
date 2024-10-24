import streamlit as st
from datetime import datetime

# Import your LangGraph workflow function
from backend import create_network_flow


# Streamlit UI
st.set_page_config(page_title="Network Automation UI", layout="wide")
st.title("\U0001F916 Network Automation with AI")

# Workflow creation
network_flow = create_network_flow()

# User Input Section
st.header("1. \U0001F4DD Enter Your Query")
query = st.text_area("Enter a network automation request:", placeholder="e.g., Show all interfaces and configure Loopback 1 with IP 1.1.1.1/24")

if st.button("Submit Query \U0001F680"):
    if query:
        # Invoke LangGraph workflow
        with st.spinner("Processing your query, please wait... \U000023F3"):
            try:
                result = network_flow.invoke({
                    "query": query,
                    "timestamp": datetime.now().isoformat()
                })
                st.success("Query processed successfully! \U0001F44D")

                # Display Command Execution Section
                st.header("2. \U0001F4BB Commands to Execute")
                for command_type, commands in result["commands"].items():
                    st.subheader(f"{command_type.capitalize()} Commands")
                    st.code("\n".join(commands), language="bash")

                # Display Results Section
                st.header("3. \U0001F50E Execution Results")
                st.markdown("<style>textarea {background-color: black; color: white; font-family: monospace;}</style>", unsafe_allow_html=True)
                for r in result["execution_results"]:
                    st.subheader(f"Command Type: {r['type'].upper()}")
                    st.text(f"Command: {r['command']}")
                    st.markdown(f"**Status**: {r['status']}")
                    st.text_area("Output", value=r['output'], height=150, label_visibility="collapsed", placeholder="Command output...")
                    st.markdown("---")

            except Exception as e:
                st.error(f"Error processing query: {str(e)} \U0001F6AB")
    else:
        st.warning("Please enter a valid query to continue. \U000026A0")
