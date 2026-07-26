
# Itinerary Processor - Codespaces Setup

## Quick Start

1. Open this repository in GitHub Codespaces
2. The container will automatically:
   - Install system dependencies (Java 17, Python 3.11)
   - Install Android build tools via Buildozer
   - Initialize the buildozer configuration

## Building the Mobile App

Once the container is ready (after setup completes):

```bash
cd mobile
buildozer -v android debug
```

The build process will:
- Compile the Python code using Kivy framework
- Package it as an Android APK
- Place output at: `mobile/bin/ItineraryDriver-0.1-debug.apk`

## Accessing Services

- **API Server**: Available on port 8000 (when running)
- **Web UI**: Available on port 8080 (when running)

## Troubleshooting

### Container startup fails
- Check the terminal output for specific error messages
- Common issues: insufficient disk space, network connectivity
- Try rebuilding the container from the Codespaces interface

### Buildozer initialization hangs
- The first build can take 20+ minutes as it downloads the entire Android SDK
- Monitor progress in the terminal

### File permissions errors
- The container runs as root, but some Android tools may require specific permissions
- Verify Java and Python paths: `which java python3`

## Manual Setup (if needed)

```bash
# Install additional Python dependencies
pip install fastapi uvicorn geopy scikit-learn pandas googlemaps folium numpy

# Start the API server
cd /workspaces/itinerary-processor
python -m uvicorn api.handler:app --host 0.0.0.0 --port 8000
```
