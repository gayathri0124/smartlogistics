import streamlit as st
import pandas as pd
from data.mock_shipments import generate_mock_data

st.set_page_config(
    page_title="Logistics Predictor",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🚚 Smart Logistics Platform")
    
    # Initialize session state
    if 'shipment_data' not in st.session_state:
        st.session_state.shipment_data = generate_mock_data()
    
    # Dashboard Overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Active Shipments",
            value=len(st.session_state.shipment_data[
                st.session_state.shipment_data['status'] != 'Delivered'
            ]),
            delta="5 new"
        )
    
    with col2:
        st.metric(
            label="On-Time Delivery Rate",
            value="94%",
            delta="2%"
        )
    
    with col3:
        st.metric(
            label="Average Delay",
            value="1.2 hours",
            delta="-0.5 hours"
        )
    
    # Recent Shipments Table
    st.subheader("Recent Shipments")
    st.dataframe(
        st.session_state.shipment_data.head(5)[
            ['shipment_id', 'origin', 'destination', 'status', 'predicted_delay']
        ],
        use_container_width=True
    )
    
    # Quick Actions
    st.subheader("Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("📦 New Shipment")
    with col2:
        st.button("🔄 Refresh Data")

if __name__ == "__main__":
    main()
