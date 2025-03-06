import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_data(n_samples=100):
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
              'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    
    statuses = ['In Transit', 'Delivered', 'Delayed', 'Processing']
    weather_conditions = ['Clear', 'Rain', 'Snow', 'Storm']
    
    data = {
        'shipment_id': [f'SHP{str(i).zfill(6)}' for i in range(n_samples)],
        'origin': np.random.choice(cities, n_samples),
        'destination': np.random.choice(cities, n_samples),
        'status': np.random.choice(statuses, n_samples, p=[0.4, 0.3, 0.2, 0.1]),
        'departure_time': [
            datetime.now() - timedelta(days=np.random.randint(0, 10))
            for _ in range(n_samples)
        ],
        'estimated_arrival': [
            datetime.now() + timedelta(days=np.random.randint(1, 5))
            for _ in range(n_samples)
        ],
        'weather_condition': np.random.choice(weather_conditions, n_samples),
        'distance_km': np.random.uniform(100, 3000, n_samples),
        'predicted_delay': np.random.uniform(0, 5, n_samples)
    }
    
    df = pd.DataFrame(data)
    return df
