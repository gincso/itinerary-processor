# API Reference

## Plugin Endpoints

`POST /api/itinerary_process`
- Processes uploaded itinerary file
- Accepts: Multipart form with `file` field
- Returns:
  ```json
  {
    "status": "success|error",
    "csv_path": "path/to/optimized_route.csv",
    "map_path": "path/to/optimized_route.html"
  }
  ```

## GitHub Actions Inputs

`itinerary`
- Path to itinerary file (default: `itinerary.md`)
- Can be set via workflow_dispatch

## Environment Variables

`GOOGLE_API_KEY`
- Required for geocoding and routing
- Can be set in:
  - Agent Zero plugin settings
  - GitHub repository secrets
