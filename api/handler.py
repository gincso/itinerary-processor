from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import re
from geopy.distance import geodesic
from datetime import datetime, timedelta
import os
import uuid
import time

async def itinerary_process(file: UploadFile = File(...)):
    """Process uploaded itinerary file and return optimized route"""
    try:
        # Create unique processing directory
        process_id = str(uuid.uuid4())
        work_dir = f"/a0/usr/workdir/itinerary_processor/{process_id}"
        os.makedirs(work_dir, exist_ok=True)

        # Save uploaded file
        file_path = f"{work_dir}/uploaded_itinerary.md"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Process itinerary
        csv_path, map_path = await process_itinerary_with_traffic(file_path, work_dir)

        return JSONResponse({
            "status": "success",
            "csv_path": csv_path,
            "map_path": map_path
        })
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

async def process_itinerary(file_path, work_dir):
    """Full itinerary processing pipeline"""

    # 1. Extract addresses from itinerary
    with open(file_path, 'r') as f:
        content = f.read()

    address_pattern = r'\|.*?\|.*?\|.*?\|(.*?)<br>.*?\|.*?\|'
    addresses = re.findall(address_pattern, content)
    cleaned_addresses = [addr.strip() + ", COTTONWOOD, AZ" for addr in addresses if addr.strip()]

    # 2. Geocode addresses (simplified - would use Google API in production)
    geocoded = []
    for i, addr in enumerate(cleaned_addresses):
        # Mock geocoding - in production would call Google Maps API
        lat = 34.73 + (i * 0.001)
        lng = -112.0 - (i * 0.001)
        geocoded.append({
            'original_address': addr,
            'formatted_address': addr,
            'lat': lat,
            'lng': lng
        })

    # 3. Calculate route with time windows
    route_plan = []
    start_time = datetime.strptime("13:00", "%H:%M")
    current_time = start_time
    avg_speed_mph = 30
    stop_time = timedelta(minutes=5)

    for i, loc in enumerate(geocoded):
        if i > 0:
            # Calculate straight-line distance
            prev_loc = (geocoded[i-1]['lat'], geocoded[i-1]['lng'])
            curr_loc = (loc['lat'], loc['lng'])
            distance_miles = geodesic(prev_loc, curr_loc).miles
            travel_time = timedelta(hours=distance_miles/avg_speed_mph)
            current_time += travel_time

        route_plan.append({
            'stop_number': i+1,
            'address': loc['original_address'],
            'formatted_address': loc['formatted_address'],
            'lat': loc['lat'],
            'lng': loc['lng'],
            'arrival_time': current_time.strftime("%H:%M"),
            'departure_time': (current_time + stop_time).strftime("%H:%M")
        })

        current_time += stop_time

    # 4. Save results
    csv_path = f"{work_dir}/optimized_route.csv"
    pd.DataFrame(route_plan).to_csv(csv_path, index=False)

    # 5. Create map visualization
    map_path = f"{work_dir}/optimized_route.html"
    create_map(route_plan, map_path)

    return csv_path, map_path

def create_map(route_plan, output_path):
    """Generate interactive map visualization"""
    import folium

    # Create map centered on first location
    m = folium.Map(location=[route_plan[0]['lat'], route_plan[0]['lng']], zoom_start=13)

    # Add markers
    for stop in route_plan:
        folium.Marker(
            location=[stop['lat'], stop['lng']],
            popup=f"Stop {stop['stop_number']}: {stop['address']}",
            icon=folium.Icon(
                color='green' if stop['stop_number'] == 1 else 
                     'red' if stop['stop_number'] == len(route_plan) else 'blue'
            )
        ).add_to(m)

    # Draw route line
    folium.PolyLine(
        locations=[[stop['lat'], stop['lng']] for stop in route_plan],
        color='blue',
        weight=5
    ).add_to(m)

    # Save map
    m.save(output_path)

def get_google_api_key():
    """Get Google Maps API key from environment or secrets"""
    # Check environment first
    key = os.getenv('GOOGLE_API_KEY')

    # Fallback to plugin config (for Agent Zero)
    if not key:
        try:
            from helpers.plugins import get_plugin_config
            config = get_plugin_config("itinerary_processor") or {}
            key = config.get("google_api_key")
        except ImportError:
            pass

    return key


def get_traffic_aware_route(origin, destination, departure_time, api_key):
    """Get route with traffic data from Google Maps API"""
    import googlemaps

    client = googlemaps.Client(key=api_key)

    try:
        directions = client.directions(
            origin=origin,
            destination=destination,
            mode="driving",
            departure_time=departure_time,
            traffic_model="best_guess"
        )

        if directions:
            return {
                'distance': directions[0]['legs'][0]['distance']['value'],  # meters
                'duration': directions[0]['legs'][0]['duration_in_traffic']['value'],  # seconds
                'polyline': directions[0]['overview_polyline']['points']
            }
    except Exception as e:
        print(f"Traffic API error: {str(e)}")
    return None

async def process_itinerary_with_traffic(file_path, work_dir):
    """Enhanced processing with traffic data"""
    api_key = get_google_api_key()
    if not api_key:
        raise ValueError("Google Maps API key required for traffic-aware routing")

    # Original processing steps
    with open(file_path, 'r') as f:
        content = f.read()

    address_pattern = r'\|.*?\|.*?\|.*?\|(.*?)<br>.*?\|.*?\|'
    addresses = re.findall(address_pattern, content)
    cleaned_addresses = [addr.strip() + ", COTTONWOOD, AZ" for addr in addresses if addr.strip()]

    # Geocode with Google Maps API
    geocoded = []
    client = googlemaps.Client(key=api_key)
    for addr in cleaned_addresses:
        try:
            geocode_result = client.geocode(addr)
            if geocode_result:
                loc = geocode_result[0]['geometry']['location']
                geocoded.append({
                    'original_address': addr,
                    'formatted_address': geocode_result[0]['formatted_address'],
                    'lat': loc['lat'],
                    'lng': loc['lng']
                })
        except Exception as e:
            print(f"Geocoding error for {addr}: {str(e)}")

    # Traffic-aware routing
    route_plan = []
    start_time = datetime.strptime("13:00", "%H:%M")
    current_time = start_time

    for i in range(len(geocoded)):
        if i > 0:
            origin = (geocoded[i-1]['lat'], geocoded[i-1]['lng'])
            destination = (geocoded[i]['lat'], geocoded[i]['lng'])

            route = get_traffic_aware_route(
                origin=origin,
                destination=destination,
                departure_time=current_time,
                api_key=api_key
            )

            if route:
                travel_time = timedelta(seconds=route['duration'])
                current_time += travel_time
            else:
                # Fallback to straight-line distance
                distance_miles = geodesic(origin, destination).miles
                travel_time = timedelta(hours=distance_miles/30)  # 30 mph default
                current_time += travel_time

        route_plan.append({
            'stop_number': i+1,
            'address': geocoded[i]['original_address'],
            'formatted_address': geocoded[i]['formatted_address'],
            'lat': geocoded[i]['lat'],
            'lng': geocoded[i]['lng'],
            'arrival_time': current_time.strftime("%H:%M"),
            'departure_time': (current_time + timedelta(minutes=5)).strftime("%H:%M")
        })

        current_time += timedelta(minutes=5)  # Stop duration

    # Save results
    csv_path = f"{work_dir}/optimized_route.csv"
    pd.DataFrame(route_plan).to_csv(csv_path, index=False)

    # Create map with traffic data
    map_path = f"{work_dir}/optimized_route.html"
    create_traffic_map(route_plan, map_path)

    return csv_path, map_path

def create_traffic_map(route_plan, output_path):
    """Generate map with traffic-aware route"""
    import folium

    m = folium.Map(location=[route_plan[0]['lat'], route_plan[0]['lng']], zoom_start=13)

    # Add markers
    for stop in route_plan:
        folium.Marker(
            location=[stop['lat'], stop['lng']],
            popup=f"Stop {stop['stop_number']}: {stop['address']}",
            icon=folium.Icon(
                color='green' if stop['stop_number'] == 1 else 
                     'red' if stop['stop_number'] == len(route_plan) else 'blue'
            )
        ).add_to(m)

    # Draw route line
    folium.PolyLine(
        locations=[[stop['lat'], stop['lng']] for stop in route_plan],
        color='blue',
        weight=5
    ).add_to(m)

    m.save(output_path)
