import streamlit as st
import folium
from streamlit_folium import folium_static
from utils.ml_utils import optimize_route
from utils.viz_utils import get_city_coords, create_shipment_map

def render_route_optimization():
    st.title("🗺️ Route Optimization")
    
    # Route Planning
    st.subheader("Plan Optimal Route")
    
    col1, col2 = st.columns(2)
    
    with col1:
        origin = st.selectbox(
            "Origin",
            options=['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
            key='origin'
        )
    
    with col2:
        destination = st.selectbox(
            "Destination",
            options=['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
            key='dest'
        )
    
    # Waypoints
    waypoints = st.multiselect(
        "Add Waypoints",
        options=['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    )
    
    if st.button("Optimize Route"):
        optimized_route, estimated_time = optimize_route(
            origin,
            destination,
            waypoints
        )
        
        # Create map with optimized route
        m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
        
        # Add markers for all points
        route_points = [origin] + optimized_route + [destination]
        
        for i in range(len(route_points) - 1):
            # Add markers
            folium.Marker(
                get_city_coords(route_points[i]),
                popup=route_points[i]
            ).add_to(m)
            
            # Draw route lines
            folium.PolyLine(
                locations=[
                    get_city_coords(route_points[i]),
                    get_city_coords(route_points[i + 1])
                ],
                color='red',
                weight=2,
                opacity=0.8
            ).add_to(m)
        
        # Add final destination marker
        folium.Marker(
            get_city_coords(destination),
            popup=destination
        ).add_to(m)
        
        # Display results
        st.success(f"Estimated delivery time: {estimated_time} hours")
        folium_static(m)
    
    # Historical Routes Analysis
    st.subheader("Popular Routes Analysis")
    
    popular_routes = st.session_state.shipment_data.groupby(
        ['origin', 'destination']
    ).size().reset_index(name='count')
    popular_routes = popular_routes.sort_values('count', ascending=False).head(5)
    
    st.dataframe(popular_routes, use_container_width=True)

if __name__ == "__main__":
    render_route_optimization()
