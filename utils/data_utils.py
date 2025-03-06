import pandas as pd
from datetime import datetime, timedelta

def calculate_performance_metrics(shipment_data):
    """Calculate key performance metrics from shipment data"""
    total_shipments = len(shipment_data)
    delayed_shipments = len(shipment_data[shipment_data['predicted_delay'] > 2])
    on_time_rate = (total_shipments - delayed_shipments) / total_shipments * 100
    
    metrics = {
        'total_shipments': total_shipments,
        'delayed_shipments': delayed_shipments,
        'on_time_rate': on_time_rate,
        'avg_delay': shipment_data['predicted_delay'].mean()
    }
    return metrics

def filter_shipments(shipment_data, status=None, date_range=None):
    """Filter shipment data based on criteria"""
    filtered_data = shipment_data.copy()
    
    if status:
        filtered_data = filtered_data[filtered_data['status'] == status]
    
    if date_range:
        start_date, end_date = date_range
        filtered_data = filtered_data[
            (filtered_data['departure_time'] >= start_date) &
            (filtered_data['departure_time'] <= end_date)
        ]
    
    return filtered_data

def get_weather_impact(shipment_data):
    """Analyze impact of weather on shipping delays"""
    weather_impact = shipment_data.groupby('weather_condition')[
        'predicted_delay'
    ].agg(['mean', 'count']).round(2)
    return weather_impact
