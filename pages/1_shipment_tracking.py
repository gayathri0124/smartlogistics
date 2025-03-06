import streamlit as st
import folium
from streamlit_folium import folium_static
from utils.viz_utils import create_shipment_map
from utils.data_utils import filter_shipments
from utils.llm_utils import analyze_shipment_status
import json

def render_tracking_page():
    st.title("📍 Shipment Tracking")

    # Filters Section
    with st.expander("📊 Filter Shipments", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            origin_filter = st.selectbox(
                "Filter by Origin",
                options=['All'] + sorted(st.session_state.shipment_data['origin'].unique().tolist())
            )

        with col2:
            destination_filter = st.selectbox(
                "Filter by Destination",
                options=['All'] + sorted(st.session_state.shipment_data['destination'].unique().tolist())
            )

        with col3:
            status_filter = st.selectbox(
                "Filter by Status",
                options=['All'] + sorted(st.session_state.shipment_data['status'].unique().tolist())
            )

    # Apply filters
    filtered_data = st.session_state.shipment_data.copy()
    if origin_filter != 'All':
        filtered_data = filtered_data[filtered_data['origin'] == origin_filter]
    if destination_filter != 'All':
        filtered_data = filtered_data[filtered_data['destination'] == destination_filter]
    if status_filter != 'All':
        filtered_data = filtered_data[filtered_data['status'] == status_filter]

    # Shipment ID Search
    shipment_id = st.text_input("Enter Shipment ID")

    if shipment_id:
        shipment = filtered_data[filtered_data['shipment_id'] == shipment_id]

        if not shipment.empty:
            shipment = shipment.iloc[0]

            # Get AI analysis
            with st.spinner("Analyzing shipment status..."):
                analysis = json.loads(analyze_shipment_status(shipment))

            # Shipment Details with AI Analysis
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Shipment Details")
                st.write(f"Origin: {shipment['origin']}")
                st.write(f"Destination: {shipment['destination']}")
                st.write(f"Current Status: {analysis['updated_status']}")
                st.write(f"Weather: {shipment['weather_condition']}")

                # Risk Level Indicator
                risk_color = {
                    "Low": "green",
                    "Medium": "yellow",
                    "High": "red"
                }.get(analysis['risk_level'], "gray")

                st.markdown(f"""
                    <div style='padding: 10px; background-color: {risk_color}; border-radius: 5px;'>
                        Risk Level: {analysis['risk_level']}
                    </div>
                    """, unsafe_allow_html=True)

            with col2:
                st.subheader("Timing")
                st.write(f"Departure: {shipment['departure_time']}")
                st.write(f"Estimated Arrival: {shipment['estimated_arrival']}")
                st.write(f"Predicted Delay: {shipment['predicted_delay']:.1f} hours")

                # AI Recommendations
                st.subheader("AI Recommendations")
                for rec in analysis['recommendations']:
                    st.write(f"• {rec}")

            # Map
            st.subheader("Route Map")
            shipment_map = create_shipment_map(shipment.to_frame().T)
            folium_static(shipment_map)
        else:
            st.error("Shipment not found")

    # All Active Shipments with applied filters
    st.subheader(f"Shipments ({len(filtered_data)} results)")
    st.dataframe(
        filtered_data[
            ['shipment_id', 'origin', 'destination', 'status', 'predicted_delay']
        ],
        use_container_width=True
    )

if __name__ == "__main__":
    render_tracking_page()