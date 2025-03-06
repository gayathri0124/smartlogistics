import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ml_utils import DelayPredictor
from utils.viz_utils import create_delay_histogram
from datetime import datetime, timedelta
from utils.llm_utils import generate_delay_insights

def render_predictions_page():
    st.title("🔮 Delay Predictions")

    # Initialize ML model
    predictor = DelayPredictor()

    # New Shipment Prediction
    st.subheader("Predict Delay for New Shipment")

    col1, col2 = st.columns(2)

    with col1:
        origin = st.selectbox(
            "Origin",
            options=['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
        )
        departure_time = st.time_input("Departure Time")
        distance = st.number_input("Distance (km)", min_value=100, max_value=3000)

    with col2:
        destination = st.selectbox(
            "Destination",
            options=['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
        )
        weather = st.selectbox(
            "Weather Condition",
            options=['Clear', 'Rain', 'Snow', 'Storm']
        )

    if st.button("Predict Delay"):
        # Create sample data for prediction
        sample_data = pd.DataFrame({
            'distance_km': [distance],
            'weather_condition': [weather],
            'departure_time': [datetime.combine(datetime.today(), departure_time)]
        })

        predicted_delay = predictor.predict_delay(sample_data)[0]

        st.info(f"Predicted Delay: {predicted_delay:.1f} hours")

        # Get AI insights
        with st.spinner("Generating AI insights..."):
            insights = generate_delay_insights(st.session_state.shipment_data)
            st.success("AI Analysis Complete!")
            st.write("🤖 AI Insights:")
            st.write(insights)

    # Historical Delay Analysis
    st.subheader("Historical Delay Analysis")

    # Delay distribution
    delay_hist = create_delay_histogram(
        st.session_state.shipment_data['predicted_delay']
    )
    st.plotly_chart(delay_hist, use_container_width=True)

    # Weather impact analysis
    weather_impact = st.session_state.shipment_data.groupby('weather_condition')[
        'predicted_delay'
    ].mean().round(2)

    st.subheader("Weather Impact on Delays")
    fig = px.bar(
        weather_impact,
        title="Average Delay by Weather Condition",
        labels={'value': 'Average Delay (hours)'}
    )
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    render_predictions_page()