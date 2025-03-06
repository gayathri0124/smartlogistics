import streamlit as st
import pandas as pd
from data.mock_shipments import generate_mock_data
from datetime import datetime
from utils.export_utils import generate_csv_download_link, generate_pdf_report, parse_uploaded_csv
from utils.weather_utils import get_route_weather
from utils.notification_utils import NotificationManager

st.set_page_config(
    page_title="Logistics Predictor",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def create_new_shipment():
    st.session_state.show_new_shipment = True
    st.session_state.shipment_created = False

def refresh_data():
    st.session_state.shipment_data = generate_mock_data()
    st.session_state.last_refresh = datetime.now()
    st.success("Data refreshed successfully!")

def main():
    st.title("🚚 Smart Logistics Platform")

    # Initialize session state
    if 'shipment_data' not in st.session_state:
        st.session_state.shipment_data = generate_mock_data()
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    if 'show_new_shipment' not in st.session_state:
        st.session_state.show_new_shipment = False

    # Batch Upload Section
    st.sidebar.subheader("📤 Batch Operations")
    uploaded_file = st.sidebar.file_uploader("Upload Shipments CSV", type="csv")
    if uploaded_file is not None:
        df, error = parse_uploaded_csv(uploaded_file)
        if error:
            st.sidebar.error(error)
        else:
            if st.sidebar.button("Process Uploaded Shipments"):
                st.session_state.shipment_data = pd.concat([df, st.session_state.shipment_data], ignore_index=True)
                st.sidebar.success(f"Added {len(df)} new shipments!")

    # Export Options
    export_format = st.sidebar.selectbox("Export Format", ["CSV", "PDF"])
    if st.sidebar.button("Export Data"):
        if export_format == "CSV":
            href = generate_csv_download_link(st.session_state.shipment_data)
            st.sidebar.markdown(f'<a href="{href}" download="shipments.csv">Download CSV</a>', unsafe_allow_html=True)
        else:
            pdf_html = generate_pdf_report(st.session_state.shipment_data)
            st.sidebar.download_button(
                "Download PDF",
                pdf_html,
                "shipments.pdf",
                "text/html"
            )

    # Dashboard Overview
    col1, col2, col3 = st.columns(3)

    with col1:
        active_shipments = len(st.session_state.shipment_data[
            st.session_state.shipment_data['status'] != 'Delivered'
        ])
        st.metric(
            label="Active Shipments",
            value=active_shipments,
            delta=f"{active_shipments - 95}"  # Example baseline
        )

    with col2:
        on_time_rate = (len(st.session_state.shipment_data[
            st.session_state.shipment_data['predicted_delay'] < 2
        ]) / len(st.session_state.shipment_data) * 100)
        st.metric(
            label="On-Time Delivery Rate",
            value=f"{on_time_rate:.1f}%",
            delta="2%"
        )

    with col3:
        avg_delay = st.session_state.shipment_data['predicted_delay'].mean()
        st.metric(
            label="Average Delay",
            value=f"{avg_delay:.1f} hours",
            delta="-0.5 hours"
        )

    # Recent Shipments Table with Weather Info
    st.subheader("Recent Shipments")
    recent_shipments = st.session_state.shipment_data.head(5)

    for _, shipment in recent_shipments.iterrows():
        with st.expander(f"Shipment {shipment['shipment_id']}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"Origin: {shipment['origin']}")
                st.write(f"Destination: {shipment['destination']}")
                st.write(f"Status: {shipment['status']}")

            with col2:
                # Get real-time weather data
                weather_info = get_route_weather(shipment['origin'], shipment['destination'])
                st.write("📍 Origin Weather:", weather_info['origin']['weather']['condition'])
                st.write("🎯 Destination Weather:", weather_info['destination']['weather']['condition'])
                if weather_info['route_risk']['risk_level'] != 'Low':
                    st.warning(f"Weather Risk: {weather_info['route_risk']['risk_level']}")

    # Quick Actions
    st.subheader("Quick Actions")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📦 New Shipment", on_click=create_new_shipment):
            pass

    with col2:
        if st.button("🔄 Refresh Data", on_click=refresh_data):
            pass

    # Show last refresh time
    st.caption(f"Last updated: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Notifications have been removed from this version

    # New Shipment Form
    if st.session_state.show_new_shipment:
        st.subheader("Create New Shipment")
        with st.form("new_shipment_form"):
            col1, col2 = st.columns(2)
            with col1:
                origin = st.selectbox(
                    "Origin",
                    options=['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
                )
                departure_time = st.time_input("Departure Time")
            with col2:
                destination = st.selectbox(
                    "Destination",
                    options=['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
                )
                weather = st.selectbox(
                    "Weather Condition",
                    options=['Clear', 'Rain', 'Snow', 'Storm']
                )

            if st.form_submit_button("Create Shipment"):
                # Add new shipment to the data
                new_data = pd.DataFrame({
                    'shipment_id': [f'SHP{len(st.session_state.shipment_data):06d}'],
                    'origin': [origin],
                    'destination': [destination],
                    'status': ['Processing'],
                    'departure_time': [datetime.combine(datetime.today(), departure_time)],
                    'weather_condition': [weather],
                    'predicted_delay': [0.0]
                })
                st.session_state.shipment_data = pd.concat(
                    [new_data, st.session_state.shipment_data],
                    ignore_index=True
                )

                st.success("New shipment created successfully!")
                st.session_state.show_new_shipment = False
                st.session_state.shipment_created = True

if __name__ == "__main__":
    main()