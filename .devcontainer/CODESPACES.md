
# Itinerary Processor - Codespaces Setup

1. Open this repository in GitHub Codespaces
2. The container will automatically:
   - Install Android tools
   - Set up Java 17
   - Install Python and Buildozer
3. Build the APK:
   ```bash
   cd mobile
   buildozer -v android debug
   ```
4. Download the APK from:
   `mobile/bin/ItineraryDriver-0.1-debug.apk`
