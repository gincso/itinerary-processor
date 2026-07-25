# Itinerary Processor - User Guide

## Table of Contents
1. [Agent Zero Plugin Installation](#agent-zero-plugin-installation)
2. [GitHub Actions Setup](#github-actions-setup)
3. [Usage Instructions](#usage-instructions)
4. [Troubleshooting](#troubleshooting)

## Agent Zero Plugin Installation

### Requirements
- Agent Zero v1.2.0 or later
- Python 3.13

### Installation Steps
1. Clone the repository to your plugins folder:
   ```bash
   git clone https://github.com/gincso/itinerary-processor.git      /a0/usr/plugins/itinerary_processor
   ```
2. Restart Agent Zero
3. Navigate to Settings > Plugins
4. Enable "Itinerary Processor"

## GitHub Actions Setup

1. Add this repository to your project as a submodule:
   ```bash
   git submodule add https://github.com/gincso/itinerary-processor.git
   ```
2. Add your Google Maps API key as a repository secret:
   - Go to Settings > Secrets > Actions
   - Add new secret named `GOOGLE_API_KEY`

## Usage Instructions

### Agent Zero Plugin
1. Open the Itinerary Processor plugin
2. Upload your itinerary file (Markdown or CSV format)
3. View/download the optimized route and map

### GitHub Actions
1. Commit an `itinerary.md` file to your repository
2. The workflow will automatically:
   - Process the itinerary
   - Create optimized route CSV
   - Generate interactive map
   - Open PR with results (if on main branch)
3. Download artifacts from the workflow run

## Troubleshooting

### Common Issues
1. **Geocoding fails**
   - Verify your Google Maps API key
   - Check address formatting in your itinerary

2. **Plugin not appearing**
   - Ensure the plugin is in `/a0/usr/plugins/`
   - Check `plugin.yaml` exists
   - Restart Agent Zero


## Traffic-Aware Routing

The plugin now supports real-time traffic data when a Google Maps API key is provided.

### Features
- Accurate ETAs based on current/predicted traffic
- Fallback to straight-line distance if API fails
- Traffic data shown on interactive map

### Requirements
- Valid Google Maps API key with:
  - Directions API enabled
  - Distance Matrix API enabled


## Multi-Driver Support

The plugin can now split large itineraries across multiple drivers.

### Features
- Automatic stop clustering using k-means
- Individual optimized routes per driver
- Color-coded map visualization

### Usage
1. Select number of drivers in the web interface
2. Upload itinerary as usual
3. View/download separate routes


## Mobile App Integration

Drivers can now access their routes via mobile devices.

### Features
- Dedicated API endpoint per driver
- JSON format optimized for mobile apps
- Real-time route updates

### Usage
1. Process itinerary as usual
2. Share driver-specific links with your team
3. Access routes from any mobile device


## Live GPS Tracking

Real-time driver locations are now visible on the map.

### Features
- WebSocket-based updates
- Color-coded driver markers
- Automatic map centering

### Mobile Integration
Drivers can submit their location via:
```
POST /api/itinerary/location
{
    "driver_id": 1,
    "lat": 34.73,
    "lng": -112.0
}
```


## Mobile APK

A driver mobile app is available for real-time tracking:

### Features
- View assigned route
- Submit location updates
- Automatic periodic updates

### Installation
1. Build the APK using the instructions in `mobile/BUILD_INSTRUCTIONS.md`
2. Transfer APK to Android device
3. Enable "Unknown Sources" in Android settings
4. Install and open the app
5. Enter your Agent Zero server URL and Driver ID


## Automated APK Builds

The APK is now automatically built:
1. On every commit to `mobile/` directory
2. When creating a new GitHub release

Pre-built APKs are available in the Actions artifacts and Releases page.


## Docker Build

For reliable builds, use the Docker method:

```bash
cd /a0/usr/plugins/itinerary_processor/mobile
./build_with_docker.sh
```

This uses a pre-configured Android environment.
