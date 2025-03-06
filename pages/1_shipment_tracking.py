import streamlit as st
import folium
from streamlit_folium import folium_static
from utils.viz_utils import create_shipment_map
from utils.data_utils import filter_shipments

def render_tracking_page():
    st.title("📍 Shipment Tracking")
    
    # Shipment ID Search
    shipment_id = st.text_input("Enter Shipment ID")
    
    if shipment_id:
        shipment = st.session_state.shipment_data[
            st.session_state.shipment_data['shipment_id'] == shipment_id
        ]
        
        if not shipment.empty:
            shipment = shipment.iloc[0]
            
            # Shipment Details
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Shipment Details")
                st.write(f"Origin: {shipment['origin']}")
                st.write(f"Destination: {shipment['destination']}")
                st.write(f"Status: {shipment['status']}")
                st.write(f"Weather: {shipment['weather_condition']}")
            
            with col2:
                st.subheader("Timing")
                st.write(f"Departure: {shipment['departure_time']}")
                st.write(f"Estimated Arrival: {shipment['estimated_arrival']}")
                st.write(f"Predicted Delay: {shipment['predicted_delay']:.1f} hours")
            
            # Map
            st.subheader("Route Map")
            shipment_map = create_shipment_map(shipment.to_frame().T)
            folium_static(shipment_map)
        else:
            st.error("Shipment not found")
    
    # All Active Shipments
    st.subheader("Active Shipments")
    active_shipments = filter_shipments(
        st.session_state.shipment_data,
        status="In Transit"
    )
    st.dataframe(
        active_shipments[
            ['shipment_id', 'origin', 'destination', 'status', 'predicted_delay']
        ],
        use_container_width=True
    )

if __name__ == "__main__":
    render_tracking_page()
