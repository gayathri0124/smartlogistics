import os
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

def analyze_shipment_status(shipment_data):
    """
    Use OpenAI to analyze shipment data and provide intelligent status updates
    """
    try:
        # Basic analysis without API
        risk_level = "Low"
        if shipment_data['predicted_delay'] > 3:
            risk_level = "Medium"
        if shipment_data['predicted_delay'] > 5 or shipment_data['weather_condition'] in ['Storm', 'Snow']:
            risk_level = "High"

        # Try to get AI-powered analysis
        try:
            prompt = f"""Analyze this shipment data and provide a detailed status update:
            - Origin: {shipment_data['origin']}
            - Destination: {shipment_data['destination']}
            - Current Status: {shipment_data['status']}
            - Weather: {shipment_data['weather_condition']}
            - Predicted Delay: {shipment_data['predicted_delay']:.1f} hours
            - Departure Time: {shipment_data['departure_time']}

            Provide a JSON response with:
            1. updated_status: Current shipment status with detailed explanation
            2. risk_level: "Low", "Medium", or "High" based on weather, delay, and other factors
            3. recommendations: List of specific actions to mitigate delays or optimize delivery
            4. eta_confidence: Confidence score (0-1) for estimated arrival time
            5. route_analysis: Brief analysis of the chosen route and potential alternatives
            """

            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a logistics expert analyzing shipment data."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content

        except Exception as api_error:
            # Fallback to basic analysis if API fails
            return json.dumps({
                "updated_status": f"{shipment_data['status']} - {shipment_data['weather_condition']} conditions",
                "risk_level": risk_level,
                "recommendations": [
                    f"Monitor weather conditions in {shipment_data['destination']}",
                    "Consider alternative routes if delays persist",
                    "Update recipient about current status"
                ],
                "eta_confidence": 0.7 if risk_level == "Low" else 0.4,
                "route_analysis": f"Direct route from {shipment_data['origin']} to {shipment_data['destination']}"
            })

    except Exception as e:
        return json.dumps({
            "updated_status": "Status analysis unavailable",
            "risk_level": "Unknown",
            "recommendations": ["System is currently unable to provide detailed analysis"],
            "eta_confidence": 0.0,
            "route_analysis": "Analysis unavailable"
        })

def generate_delay_insights(historical_data):
    """
    Generate insights about delay patterns, with fallback to basic analysis
    """
    try:
        # Basic statistical analysis
        avg_delay = historical_data['predicted_delay'].mean()
        weather_impact = historical_data.groupby('weather_condition')['predicted_delay'].mean()
        worst_weather = weather_impact.idxmax()

        # Try AI-powered analysis
        try:
            data_summary = f"""
            Total Shipments: {len(historical_data)}
            Average Delay: {avg_delay:.1f} hours
            Weather Conditions: {', '.join(historical_data['weather_condition'].unique())}
            Most Common Routes: {', '.join(historical_data.groupby(['origin', 'destination']).size().nlargest(3).index.map(lambda x: f'{x[0]} to {x[1]}'))}
            """

            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a logistics analyst providing insights on shipping patterns."},
                    {"role": "user", "content": f"Analyze this shipping data and provide key insights:\n{data_summary}"}
                ]
            )
            return response.choices[0].message.content

        except Exception as api_error:
            # Fallback to basic insights
            return f"""📊 Basic Delay Analysis:
            • Average delay across all shipments: {avg_delay:.1f} hours
            • Weather condition causing most delays: {worst_weather}
            • {len(historical_data)} shipments analyzed

            Recommendations:
            • Monitor {worst_weather} conditions closely
            • Plan alternative routes during adverse weather
            • Consider adding buffer time for frequently delayed routes
            """

    except Exception as e:
        return "Unable to generate delay insights at this time."

def suggest_route_improvements(origin, destination, current_delay):
    """
    Suggest route improvements with fallback to basic suggestions
    """
    try:
        # Basic suggestions
        basic_recommendations = f"""
        Route Analysis: {origin} to {destination}
        • Consider weather conditions along the route
        • Monitor traffic patterns
        • Plan for alternative routes if needed
        """

        # Try AI-powered suggestions
        try:
            prompt = f"""
            Analyze this route and suggest improvements:
            - Origin: {origin}
            - Destination: {destination}
            - Current Delay: {current_delay} hours

            Provide recommendations for:
            1. Alternative routes
            2. Optimal departure times
            3. Weather considerations
            4. Risk mitigation strategies
            """

            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a route optimization expert."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content

        except Exception as api_error:
            return basic_recommendations

    except Exception as e:
        return "Basic route analysis currently unavailable."