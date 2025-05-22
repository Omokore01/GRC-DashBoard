# 🚨 Incident Response Playbook & Simulation Dashboard

This interactive dashboard visualizes **cybersecurity incident response** activities using simulated data. It helps teams monitor incident types, escalation patterns, and response phase effectiveness.

Built with Dash and Plotly, it mimics a real SOC dashboard for educational and demonstration purposes.

---

## 📊 Key Features

- 📋 Tracks incidents across IR phases (Preparation → Recovery)
- 📊 Grouped bar charts showing incident volume and escalation counts
- 🧯 Simulated metrics for IR phases, incident types, and outcomes
- 📈 Funnel visualization for IR lifecycle analysis

---

## ⚙️ Technologies

- **Python 3.11+**
- **Dash** + **Dash Bootstrap Components**
- **Pandas & NumPy**
- **Plotly Express**

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/incident-response-dashboard.git
cd incident-response-dashboard
2. (Optional) Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
3. Install Requirements
pip install -r requirements.txt
Or directly:
pip install dash dash-bootstrap-components pandas numpy plotly
4. Run the App
python app_ir_dashboard.py
