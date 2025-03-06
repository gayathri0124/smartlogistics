import streamlit as st
import plotly.express as px
from utils.data_utils import calculate_performance_metrics, get_weather_impact
from utils.viz_utils import create_performance_timeline

def render_analytics_page():
    st.title("📊 Analytics Dashboard")
    
    # Date range filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")
    
    # Calculate metrics
    metrics = calculate_performance_metrics(st.session_state.shipment_data)
    
    # Display KPIs
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Shipments", metrics['total_shipments'])
    with col2:
        st.metric("Delayed Shipments", metrics['delayed_shipments'])
    with col3:
        st.metric("On-Time Rate", f"{metrics['on_time_rate']:.1f}%")
    with col4:
        st.metric("Average Delay", f"{metrics['avg_delay']:.1f} hours")
    
    # Performance Timeline
    st.subheader("Performance Timeline")
    timeline = create_performance_timeline(st.session_state.shipment_data)
    st.plotly_chart(timeline, use_container_width=True)
    
    # Weather Impact Analysis
    st.subheader("Weather Impact Analysis")
    weather_impact = get_weather_impact(st.session_state.shipment_data)
    
    fig = px.bar(
        weather_impact,
        title="Delays by Weather Condition",
        labels={'mean': 'Average Delay (hours)', 'count': 'Number of Shipments'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Route Performance
    st.subheader("Route Performance")
    route_performance = st.session_state.shipment_data.groupby(
        ['origin', 'destination']
    )['predicted_delay'].mean().reset_index()
    
    route_performance = route_performance.sort_values('predicted_delay', ascending=False)
    st.dataframe(route_performance.round(2), use_container_width=True)

if __name__ == "__main__":
    render_analytics_page()
