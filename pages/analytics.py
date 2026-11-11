"""Analytics page with interactive Plotly visualisations."""
import streamlit as st
from utils.analytics import get_inspections_df, plot_defect_distribution, plot_daily_trends, plot_status_pie

def render():
    st.title("📊 Industrial Quality Analytics")
    st.markdown("Detailed breakdown of defect frequencies, trends, and quality metrics.")

    df = get_inspections_df()
    if df.empty:
        st.info("Insufficient data to generate analytics. Please perform inspections first.")
        return

    c1, c2 = st.columns(2)
    with c1:
        fig_dist = plot_defect_distribution(df)
        if fig_dist:
            st.plotly_chart(fig_dist, use_container_width=True)
            
    with c2:
        fig_pie = plot_status_pie(df)
        if fig_pie:
            st.plotly_chart(fig_pie, use_container_width=True)

    fig_trends = plot_daily_trends(df)
    if fig_trends:
        st.plotly_chart(fig_trends, use_container_width=True)

