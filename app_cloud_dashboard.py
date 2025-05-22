import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------
# ✅ Dummy Cloud Security Findings
# -----------------------------
df = pd.DataFrame({
    'Service': np.random.choice(['EC2', 'S3', 'IAM', 'Lambda', 'RDS', 'VPC'], 50),
    'Issue': np.random.choice([
        'Open port', 'Public bucket', 'Weak password policy',
        'Excessive IAM permissions', 'Missing encryption', 'No logging enabled'
    ], 50),
    'Severity': np.random.choice(['Low', 'Medium', 'High', 'Critical'], 50),
    'Region': np.random.choice(['us-east-1', 'us-west-2', 'eu-central-1'], 50),
    'Detected On': pd.date_range(end=pd.Timestamp.today(), periods=50).strftime('%Y-%m-%d')
})

# -----------------------------
# 🧠 Dash App Setup
# -----------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
app.title = "Cloud Security Dashboard"

# -----------------------------
# 🌐 Layout
# -----------------------------
app.layout = dbc.Container([
    html.H2("☁️ Cloud Security Assessment Dashboard", className="text-center my-4"),

    html.H5("📋 Findings Table"),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        id='cloud-table'
    ),
    html.Br(),

    html.H5("📊 Findings by Cloud Service & Severity"),
    dcc.Graph(
        figure=px.histogram(
            df,
            x="Service",
            color="Severity",
            barmode="group",
            title="Service-Wise Distribution of Issues"
        )
    ),
    html.Br(),

    html.H5("🌍 Findings by AWS Region"),
    dcc.Graph(
        figure=px.pie(
            df,
            names='Region',
            title='Issues by Region',
            hole=0.3
        )
    )
], fluid=True)

# -----------------------------
# 🚀 Run App
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8051)

Run it:
!python3 app_cloud_dashboard.py

Tunnel it (in a new cell):
!./cloudflared tunnel --url http://localhost:8051

