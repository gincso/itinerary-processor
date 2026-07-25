#!/bin/bash
# Build APK using Docker

docker build -t itinerary-builder . && docker run -v $(pwd):/app itinerary-builder

# Fix permissions
sudo chown -R $USER:$USER .
