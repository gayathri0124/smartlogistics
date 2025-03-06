import os
from openai import OpenAI
from datetime import datetime

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
    1. updated_status: Current shipment status
    2. risk_level: "Low", "Medium", or "High"
    3. recommendations: List of actions to mitigate delays
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Using GPT-4 for better analysis
            messages=[
                {"role": "system", "content": "You are a logistics expert analyzing shipment data."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        return {
            "updated_status": shipment_data['status'],
            "risk_level": "Unknown",
            "recommendations": [f"Error in status analysis: {str(e)}"]
        }

def generate_delay_insights(historical_data):
    """
    Generate insights about delay patterns using LLM
    """
    data_summary = f"""
    Total Shipments: {len(historical_data)}
    Average Delay: {historical_data['predicted_delay'].mean():.1f} hours
    Weather Conditions: {', '.join(historical_data['weather_condition'].unique())}
    Most Common Routes: {', '.join(historical_data.groupby(['origin', 'destination']).size().nlargest(3).index.map(lambda x: f'{x[0]} to {x[1]}'))}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a logistics analyst providing insights on shipping patterns."},
                {"role": "user", "content": f"Analyze this shipping data and provide key insights:\n{data_summary}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating insights: {str(e)}"
