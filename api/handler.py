from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from helpers.plugins import get_plugin_config
import pandas as pd
from geopy.distance import geodesic
from datetime import datetime, timedelta
import os
import uuid

async def itinerary_process(file: UploadFile = File(...)):
    try:
        # Create unique processing directory
        process_id = str(uuid.uuid4())
        work_dir = f"/a0/usr/workdir/itinerary_processor/{process_id}"
        os.makedirs(work_dir, exist_ok=True)

        # Save uploaded file
        file_path = f"{work_dir}/uploaded_itinerary.md"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Process itinerary (using our existing logic)
        csv_path, map_path = await process_itinerary(file_path, work_dir)

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
    # Implement the processing logic we developed earlier
    # This would include:
    # 1. Address extraction
    # 2. Geocoding
    # 3. Route planning
    # 4. Saving results to CSV and HTML map

    # For now just return placeholder paths
    csv_path = f"{work_dir}/optimized_route.csv"
    map_path = f"{work_dir}/optimized_route.html"

    # Create dummy files for testing
    pd.DataFrame([{"test": "data"}]).to_csv(csv_path)
    with open(map_path, "w") as f:
        f.write("<html><body>Test map</body></html>")

    return csv_path, map_path
