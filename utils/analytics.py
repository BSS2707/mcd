"""Analytics and visualization utilities using Plotly and Pandas."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.db import get_all_inspections
from config.settings import PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, STEEL_BLUE

def get_inspections_df():
    """Fetches all inspections as a pandas DataFrame."""
    records = get_all_inspections()
    if not records:
        return pd.DataFrame()
    columns = ["id", "inspection_id", "timestamp", "image_name", "defect_count", "defect_names", "status", "detections_json"]
    df = pd.DataFrame(records, columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def plot_defect_distribution(df):
    """Generates a bar chart of defect frequencies."""
    if df.empty or 'defect_names' not in df.columns:
        return None
    
    # Split defect_names string into individual defect counts
    defects = []
    for item in df['defect_names'].dropna():
        names = [d.strip() for d in str(item).split(',') if d.strip()]
        defects.extend(names)
        
    if not defects:
        return None
        
    counts = pd.Series(defects).value_counts().reset_index()
    counts.columns = ['Defect Type', 'Count']
    
    fig = px.bar(
        counts,
        x='Defect Type',
        y='Count',
        title="Defect Frequency Distribution",
        color='Count',
        color_continuous_scale=[[0, PRIMARY_COLOR], [1, ACCENT_COLOR]]
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="sans-serif")
    )
    return fig

def plot_daily_trends(df):
    """Plots inspection count trends over time."""
    if df.empty or 'timestamp' not in df.columns:
        return None
        
    daily = df.set_index('timestamp').resample('D').size().reset_index(name='Total Inspections')
    fig = px.line(
        daily,
        x='timestamp',
        y='Total Inspections',
        title="Daily Inspection Volume",
        markers=True,
        line_shape='spline'
    )
    fig.update_traces(line_color=ACCENT_COLOR)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Date",
        yaxis_title="Inspections Count"
    )
    return fig

def plot_status_pie(df):
    """Plots pass vs fail inspection ratio."""
    if df.empty or 'status' not in df.columns:
        return None
        
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    fig = px.pie(
        status_counts,
        names='Status',
        values='Count',
        title="Inspection Results (Pass / Fail)",
        color='Status',
        color_discrete_map={'Pass': '#28a745', 'Fail': '#dc3545', 'Defective': ACCENT_COLOR}
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

