import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd

# ✅ Hardcoded dummy data (visible immediately)
df = pd.DataFrame({
    'Risk ID': ['R001', 'R002', 'R003', 'R004', 'R005'],
    'Risk Description': [
        'Unpatched OS vulnerability',
        'Phishing attack vector',
        'Open storage bucket',
        'Privilege escalation flaw',
        'Weak access controls'
    ],
    'Likelihood': [5, 4, 3, 4, 2],
    'Impact': [4, 5, 3, 4, 5],
    'Risk Score': [20, 20, 9, 16, 10],
    'Compliance Mapping': ['ISO 27001', 'NIST CSF', 'HIPAA', 'SOC 2', 'PCI DSS'],
    'Status': ['Open', 'In Progress', 'Mitigated', 'Open', 'Open']
})

# App layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "GRC Dashboard"
app.layout = dbc.Container([
    html.H2("🛡️ GRC Dashboard", className="my-4 text-center"),
    dcc.Dropdown(
        id='status-filter',
        options=[{'label': s, 'value': s} for s in df['Status'].unique()],
        value=list(df['Status'].unique()),  # default: all selected
        multi=True,
        placeholder="Filter by Status"
    ),
    html.Br(),
    dash_table.DataTable(
        id='risk-table',
        columns=[{"name": col, "id": col} for col in df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        page_size=10
    ),
    html.Br(),
    dcc.Graph(id='risk-bar'),
    html.Br(),
    dcc.Graph(id='compliance-pie')
], fluid=True)

@app.callback(
    [Output('risk-table', 'data'),
     Output('risk-bar', 'figure'),
     Output('compliance-pie', 'figure')],
    Input('status-filter', 'value')
)
def update_dashboard(selected_statuses):
    filtered = df[df['Status'].isin(selected_statuses)]
    bar_fig = {
        "data": [{
            "x": filtered['Risk ID'],
            "y": filtered['Risk Score'],
            "type": "bar",
            "name": "Risk Score"
        }],
        "layout": {"title": "Risk Score by Risk ID"}
    }
    pie_fig = {
        "data": [{
            "labels": filtered['Compliance Mapping'].value_counts().index,
            "values": filtered['Compliance Mapping'].value_counts().values,
            "type": "pie",
            "hole": 0.4
        }],
        "layout": {"title": "Compliance Mapping Overview"}
    }
    return filtered.to_dict('records'), bar_fig, pie_fig

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050)
