import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------
# ✅ Dummy Incident Response Data
# -----------------------------
np.random.seed(42)

phases = ['Preparation', 'Detection', 'Analysis', 'Containment', 'Eradication', 'Recovery']
incident_types = ['Phishing', 'Ransomware', 'Insider Threat', 'DDoS', 'Credential Theft']

# Simulate metrics
data = {
    'Phase': np.random.choice(phases, 100),
    'Incident Type': np.random.choice(incident_types, 100),
    'Escalated': np.random.randint(0, 2, size=100)
}
df = pd.DataFrame(data)

# -----------------------------
# Dash App Setup
# -----------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])
app.title = "Incident Response Dashboard"

# -----------------------------
# Layout
# -----------------------------
app.layout = dbc.Container([
    html.H2("🚨 Incident Response Simulation Dashboard", className="text-center my-4"),

    html.H5("📊 Incident Volume by Response Phase"),
    dcc.Graph(
        figure=px.histogram(
            df, x='Phase', color='Incident Type', barmode='group',
            title='Incidents by Phase and Type'
        )
    ),
    html.Br(),

    html.H5("📈 Escalated Incidents per Phase"),
    dcc.Graph(
        figure=px.bar(
            df.groupby('Phase')['Escalated'].sum().reset_index(),
            x='Phase', y='Escalated', title='Escalated Incidents by Phase'
        )
    ),
    html.Br(),

    html.H5("📍 Funnel View of IR Lifecycle"),
    dcc.Graph(
        figure=px.funnel(
            df['Phase'].value_counts().reset_index().rename(
                columns={'index': 'Phase', 'Phase': 'Count'}
            ).sort_values('Phase'),
            x='Count', y='Phase',
            title='IR Workflow Funnel'
        )
    )

], fluid=True)

# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8052)


