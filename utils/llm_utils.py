import os
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

def analyze_shipment_status(shipment_data):
    """
    Use OpenAI to analyze shipment data and provide intelligent status updates
    """
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

    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
        response = client.chat.completions.create(
            model="gpt-4o",  # Latest model for better analysis
            messages=[
                {"role": "system", "content": "You are a logistics expert analyzing shipment data."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content  # This is already a JSON string
    except Exception as e:
        # Return a JSON string instead of a dictionary
        return json.dumps({
            "updated_status": shipment_data['status'],
            "risk_level": "Unknown",
            "recommendations": [f"Error in status analysis: {str(e)}"],
            "eta_confidence": 0.0,
            "route_analysis": "Unable to analyze route due to error"
        })

def generate_delay_insights(historical_data):
    """
    Generate comprehensive insights about delay patterns using LLM
    """
    data_summary = f"""
    Total Shipments: {len(historical_data)}
    Average Delay: {historical_data['predicted_delay'].mean():.1f} hours
    Weather Conditions: {', '.join(historical_data['weather_condition'].unique())}
    Most Common Routes: {', '.join(historical_data.groupby(['origin', 'destination']).size().nlargest(3).index.map(lambda x: f'{x[0]} to {x[1]}'))}
    Delay Distribution: {historical_data['predicted_delay'].describe().to_dict()}
    Weather Impact: {historical_data.groupby('weather_condition')['predicted_delay'].mean().to_dict()}
    """

    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": """You are a logistics analyst providing insights on shipping patterns.
                    Focus on:
                    1. Key delay patterns and their causes
                    2. Weather impact analysis
                    3. Route optimization suggestions
                    4. Specific recommendations for improving delivery times
                    5. Risk factors and mitigation strategies"""
                },
                {"role": "user", "content": f"Analyze this shipping data and provide key insights:\n{data_summary}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating insights: {str(e)}"

def suggest_route_improvements(origin, destination, current_delay):
    """
    Use LLM to suggest route improvements based on current conditions
    """
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

    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a route optimization expert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error suggesting route improvements: {str(e)}"