
## Building the Mobile APK

1. Install Buildozer:
```bash
pip install buildozer
```

2. Install Android build dependencies:
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

3. Navigate to the mobile directory:
```bash
cd /a0/usr/plugins/itinerary_processor/mobile
```

4. Initialize Buildozer:
```bash
buildozer init
```

5. Build the APK:
```bash
buildozer -v android debug
```

The APK will be created at:
`/a0/usr/plugins/itinerary_processor/mobile/bin/ItineraryDriver-0.1-debug.apk`
