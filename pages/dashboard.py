"""Dashboard view with key KPI metrics, recent defect activities, and overview charts."""
import streamlit as st
from utils.analytics import get_inspections_df, plot_defect_distribution, plot_status_pie

def render():
    st.title("🏭 Motherboard Inspection Dashboard")
    st.markdown("Real-time automated manufacturing defect intelligence & quality statistics.")
    
    df = get_inspections_df()
    
    col1, col2, col3, col4 = st.columns(4)
    if not df.empty:
        total_inspections = len(df)
        total_defects = df['defect_count'].sum()
        defect_free = (df['defect_count'] == 0).sum()
        
        # Most frequent defect
        all_defects = []
        for d_str in df['defect_names'].dropna():
            items = [d.strip() for d in str(d_str).split(',') if d.strip()]
            all_defects.extend(items)
        most_common = max(set(all_defects), key=all_defects.count) if all_defects else "None"
        
        col1.metric("Total Inspections", total_inspections)
        col2.metric("Total Defects Found", total_defects)
        col3.metric("Defect-Free Units", defect_free)
        col4.metric("Top Defect", most_common)
    else:
        col1.metric("Total Inspections", 0)
        col2.metric("Total Defects Found", 0)
        col3.metric("Defect-Free Units", 0)
        col4.metric("Top Defect", "N/A")

    st.markdown("---")
    
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        if not df.empty:
            fig_dist = plot_defect_distribution(df)
            if fig_dist:
                st.plotly_chart(fig_dist, use_container_width=True)
            else:
                st.info("No defect occurrences recorded yet to plot distribution.")
        else:
            st.info("No inspection records available.")
            
    with chart_col2:
        if not df.empty:
            fig_pie = plot_status_pie(df)
            if fig_pie:
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No status data available.")
        else:
            st.info("Run inspections to see quality stats.")

    st.markdown("### 📋 Recent Inspection Logs")
    if not df.empty:
        st.dataframe(df[['inspection_id', 'timestamp', 'image_name', 'defect_count', 'defect_names', 'status']].head(10), use_container_width=True)
    else:
        st.write("No inspections logged yet.")

