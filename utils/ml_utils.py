import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

class DelayPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_fitted = False

    def prepare_features(self, data):
        """Convert raw shipment data into ML features"""
        # Example feature engineering
        features = np.column_stack([
            data['distance_km'],
            data['weather_condition'].map({
                'Clear': 0, 'Rain': 1, 'Snow': 2, 'Storm': 3
            }),
            data['departure_time'].dt.hour,
            data['departure_time'].dt.dayofweek
        ])
        return self.scaler.fit_transform(features) if not self.is_fitted else self.scaler.transform(features)

    def fit(self, shipment_data):
        """Train the model with historical data"""
        features = self.prepare_features(shipment_data)
        # Use predicted_delay as target variable
        self.model.fit(features, shipment_data['predicted_delay'])
        self.is_fitted = True

    def predict_delay(self, shipment_data):
        """Predict shipping delays based on current conditions"""
        if not self.is_fitted:
            # Train with mock data if not fitted
            from data.mock_shipments import generate_mock_data
            training_data = generate_mock_data(1000)  # Generate more data for training
            self.fit(training_data)

        features = self.prepare_features(shipment_data)
        return self.model.predict(features)

def optimize_route(origin, destination, waypoints):
    """Route optimization using distance-based approach

    This function optimizes delivery routes between two points:
    1. Calculates distances between all points
    2. Uses a simple nearest neighbor algorithm to find the best route
    3. Returns the optimized sequence of waypoints

    Parameters:
    - origin: Starting city
    - destination: Final destination
    - waypoints: List of cities to visit

    Returns:
    - optimized_route: List of waypoints in optimal order
    - estimated_time: Estimated delivery time in hours
    """
    # Simple route optimization logic
    points = [origin] + waypoints
    optimized_route = []
    current_point = origin
    unvisited = waypoints.copy()

    while unvisited:
        # Find nearest unvisited point
        distances = [calculate_distance(current_point, p) for p in unvisited]
        nearest_idx = np.argmin(distances)
        next_point = unvisited.pop(nearest_idx)
        optimized_route.append(next_point)
        current_point = next_point

    total_distance = sum([
        calculate_distance(origin, optimized_route[0])
    ] + [
        calculate_distance(optimized_route[i], optimized_route[i+1])
        for i in range(len(optimized_route)-1)
    ] + [
        calculate_distance(optimized_route[-1], destination)
    ])

    # Estimate time based on average speed of 60 km/h
    estimated_time = total_distance / 60

    return optimized_route, estimated_time

def calculate_distance(city1, city2):
    """Calculate approximate distance between two cities"""
    from utils.viz_utils import get_city_coords

    coord1 = get_city_coords(city1)
    coord2 = get_city_coords(city2)

    # Simple Euclidean distance * scaling factor for demonstration
    dist = np.sqrt(
        (coord1[0] - coord2[0])**2 + 
        (coord1[1] - coord2[1])**2
    ) * 111  # Convert to approximate kilometers

    return dist