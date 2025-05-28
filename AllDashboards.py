pip install streamlit pandas

# Install required libraries
!pip install -q streamlit pyngrok pandas pyyaml

# Authenticate ngrok (OPTIONAL: replace with your token if needed)
from pyngrok import ngrok
ngrok.set_auth_token("")

# Kill previous tunnels if any
ngrok.kill()


%%writefile app1_grc_dashboard.py
import streamlit as st
import pandas as pd

data = {
    'Risk ID': ['R001', 'R002', 'R003'],
    'Risk Description': [
        'Unpatched server vulnerabilities',
        'Weak IAM policies',
        'Unencrypted sensitive data'
    ],
    'Likelihood': [4, 3, 5],
    'Impact': [5, 4, 5],
    'Risk Score': [20, 12, 25],
    'Compliance Mapping': ['ISO 27001 A.12.6.1', 'NIST AC-1', 'HIPAA 164.312(a)(2)(iv)'],
    'Status': ['Open', 'In Progress', 'Open']
}
df = pd.DataFrame(data)

st.set_page_config(page_title="GRC Dashboard", layout="wide")
st.title("🛡️ GRC Dashboard – Risk Register & Compliance Tracker")

with st.sidebar:
    st.header("Filter Risks")
    status_filter = st.multiselect("Status", options=df['Status'].unique(), default=df['Status'].unique())
    compliance_filter = st.multiselect("Compliance", options=df['Compliance Mapping'].unique(), default=df['Compliance Mapping'].unique())

filtered_df = df[df['Status'].isin(status_filter) & df['Compliance Mapping'].isin(compliance_filter)]

st.subheader("📋 Risk Register Table")
st.dataframe(filtered_df, use_container_width=True)

st.subheader("📊 Risk Scores by ID")
st.bar_chart(filtered_df.set_index('Risk ID')['Risk Score'])

st.subheader("✅ Compliance Framework Coverage")
compliance_counts = filtered_df['Compliance Mapping'].value_counts()
st.dataframe(compliance_counts.rename_axis("Compliance Framework").reset_index(name='# of Risks'))

st.download_button(
    label="📥 Download Filtered Risk Register",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_risk_register.csv",
    mime="text/csv"
)


%%writefile app2_cloud_assessment.py
import streamlit as st
import pandas as pd

data = {
    'Check ID': ['C001', 'C002', 'C003', 'C004'],
    'Description': [
        'S3 bucket publicly accessible',
        'IAM role allows * permissions',
        'Security group allows SSH from 0.0.0.0/0',
        'Root account MFA not enabled'
    ],
    'Service': ['S3', 'IAM', 'EC2', 'IAM'],
    'Severity': ['High', 'Critical', 'High', 'Medium'],
    'Recommendation': [
        'Restrict bucket access to private',
        'Limit IAM policy scope',
        'Restrict SSH to trusted IPs',
        'Enable MFA on root account'
    ]
}
df = pd.DataFrame(data)

st.set_page_config(page_title="Cloud Security Assessment", layout="wide")
st.title("☁️ Cloud Security Assessment Tool")

with st.sidebar:
    st.header("🔎 Filter Findings")
    selected_severity = st.multiselect("Filter by Severity", df['Severity'].unique(), default=df['Severity'].unique())

filtered_df = df[df['Severity'].isin(selected_severity)]

st.subheader("🧾 Assessment Findings")
st.dataframe(filtered_df, use_container_width=True)

st.subheader("📊 Severity Distribution")
severity_chart = filtered_df['Severity'].value_counts().rename_axis("Severity").reset_index(name="Count")
st.bar_chart(severity_chart.set_index("Severity"))

st.download_button(
    label="📥 Download Findings Report (CSV)",
    data=filtered_df.to_csv(index=False),
    file_name="cloud_security_findings.csv",
    mime="text/csv"
)


%%writefile app3_ir_playbook.py
import streamlit as st
import pandas as pd
import yaml

playbooks = {
    "Phishing Attack": [
        {"Step": 1, "Action": "Identify suspicious email", "Tool": "Email client / User report"},
        {"Step": 2, "Action": "Isolate affected user account", "Tool": "IAM / Directory Service"},
        {"Step": 3, "Action": "Scan for malware or credential use", "Tool": "EDR / SIEM"},
        {"Step": 4, "Action": "Reset credentials & notify stakeholders", "Tool": "Helpdesk / Email"}
    ],
    "Ransomware": [
        {"Step": 1, "Action": "Detect abnormal encryption behavior", "Tool": "SIEM / EDR"},
        {"Step": 2, "Action": "Isolate infected systems", "Tool": "Firewall / NAC"},
        {"Step": 3, "Action": "Initiate IR plan and snapshot system", "Tool": "Backup / VM tools"},
        {"Step": 4, "Action": "Restore from backup & notify legal", "Tool": "Backup system"}
    ]
}

st.set_page_config(page_title="IR Playbook", layout="wide")
st.title("🚨 IR Playbook & Simulation Tool")

incident = st.sidebar.selectbox("🧭 Choose an Incident Type", list(playbooks.keys()))
df = pd.DataFrame(playbooks[incident])
st.subheader(f"📋 Playbook: {incident}")
st.dataframe(df, use_container_width=True)

st.subheader("🧪 Step-by-Step Simulation")
if st.button("▶️ Start Simulation"):
    for step in playbooks[incident]:
        with st.expander(f"Step {step['Step']}: {step['Action']}"):
            st.write(f"🔧 **Tool:** {step['Tool']}")
            st.checkbox("✅ Mark as Completed")

yaml_output = yaml.dump({incident: playbooks[incident]}, sort_keys=False)
st.download_button("📥 Download YAML", data=yaml_output, file_name=f"{incident}_playbook.yaml", mime="text/yaml")


# Manually remove pyngrok config (including old token)
!rm -rf ~/.ngrok2


from pyngrok import ngrok

# Set your NEW working token
ngrok.set_auth_token("2xHWk9mCYarSJTtSiGT5JctID3P_7En3JbQSbkBqUmDz5RFKN")



import os
import subprocess
from pyngrok import ngrok
import ipywidgets as widgets
from IPython.display import display

# Dropdown to choose which app to launch
dropdown = widgets.Dropdown(
    options=[
        ("GRC Dashboard", "app1_grc_dashboard.py"),
        ("Cloud Security Assessment Tool", "app2_cloud_assessment.py"),
        ("IR Playbook & Simulator", "app3_ir_playbook.py")
    ],
    description='Select App:',
    disabled=False,
)

button = widgets.Button(description="🚀 Launch Streamlit App")

output = widgets.Output()

def on_button_clicked(b):
    with output:
        output.clear_output()
        print("🔄 Stopping any existing Streamlit process...")
        os.system("pkill streamlit")

        filename = dropdown.value
        print(f"🚀 Launching: {filename}")

        # Start the tunnel
        public_url = ngrok.connect(addr=8501, proto="http")
        print("🌐 Streamlit App URL:", public_url)

        # Launch the selected app
        subprocess.Popen(["streamlit", "run", filename])

button.on_click(on_button_clicked)

display(dropdown, button, output)
