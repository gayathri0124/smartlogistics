import streamlit as st
import plotly.express as px
from utils.data_utils import calculate_performance_metrics, get_weather_impact
from utils.viz_utils import create_performance_timeline
from datetime import datetime, timedelta
import pandas as pd

def render_analytics_page():
    st.title("📊 Performance Analytics")

    # Initialize session state if needed
    if 'shipment_data' not in st.session_state:
        from data.mock_shipments import generate_mock_data
        st.session_state.shipment_data = generate_mock_data()

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

    # Route Performance Analysis
    st.subheader("Route Performance")
    route_performance = st.session_state.shipment_data.groupby(
        ['origin', 'destination']
    )['predicted_delay'].agg(['mean', 'count']).round(2).reset_index()

    route_performance = route_performance.sort_values('mean', ascending=False)
    st.dataframe(route_performance, use_container_width=True)

    # Historical Trend Analysis
    st.subheader("Historical Trend Analysis")
    trend_data = st.session_state.shipment_data.copy()
    trend_data['date'] = pd.to_datetime(trend_data['departure_time']).dt.date
    daily_delays = trend_data.groupby('date')['predicted_delay'].mean().reset_index()

    fig_trend = px.line(
        daily_delays, 
        x='date', 
        y='predicted_delay',
        title="Daily Average Delay Trend",
        labels={'predicted_delay': 'Average Delay (hours)', 'date': 'Date'}
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # Download Reports
    st.subheader("Export Analytics")
    report_type = st.selectbox(
        "Select Report Type",
        ["Performance Summary", "Weather Impact", "Route Analysis"]
    )

    if st.button("Generate Report"):
        if report_type == "Performance Summary":
            report_data = pd.DataFrame([metrics])
        elif report_type == "Weather Impact":
            report_data = weather_impact
        else:
            report_data = route_performance

        csv = report_data.to_csv(index=False)
        st.download_button(
            "Download Report (CSV)",
            csv,
            f"{report_type.lower().replace(' ', '_')}_report.csv",
            "text/csv"
        )

if __name__ == "__main__":
    render_analytics_page()