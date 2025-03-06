import plotly.express as px
import plotly.graph_objects as go
import folium

def create_shipment_map(shipment_data):
    """Create an interactive map with shipment routes"""
    # Center the map on US
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    
    # Add shipment routes
    for _, row in shipment_data.iterrows():
        # Simple straight line between origin and destination
        folium.PolyLine(
            locations=[
                get_city_coords(row['origin']),
                get_city_coords(row['destination'])
            ],
            color='blue',
            weight=2,
            opacity=0.8
        ).add_to(m)
    
    return m

def create_delay_histogram(delays):
    """Create histogram of shipping delays"""
    fig = px.histogram(
        delays,
        nbins=20,
        title="Distribution of Shipping Delays",
        labels={'value': 'Delay (hours)', 'count': 'Number of Shipments'}
    )
    return fig

def create_performance_timeline(data):
    """Create timeline of shipping performance"""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data['departure_time'],
            y=data['predicted_delay'],
            mode='lines',
            name='Delay Trend'
        )
    )
    return fig

def get_city_coords(city):
    """Return approximate coordinates for major US cities"""
    coords = {
        'New York': [40.7128, -74.0060],
        'Los Angeles': [34.0522, -118.2437],
        'Chicago': [41.8781, -87.6298],
        'Houston': [29.7604, -95.3698],
        'Phoenix': [33.4484, -112.0740]
    }
    return coords.get(city, [39.8283, -98.5795])  # Default to US center
