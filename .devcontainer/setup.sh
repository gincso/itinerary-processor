#!/bin/bash
set -e

echo "🔧 Setting up Itinerary Processor development environment..."

# Update package lists
apt-get update

# Install Buildozer dependencies (required for Android APK building)
apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    autoconf \
    automake \
    libtool \
    pkg-config \
    git \
    wget

# Install Python build tools
pip install --upgrade pip setuptools wheel cython

# Install Buildozer
pip install buildozer

# Navigate to mobile directory if it exists
if [ -d "/workspaces/itinerary-processor/mobile" ]; then
    cd /workspaces/itinerary-processor/mobile
    
    # Initialize buildozer if not already done
    if [ ! -f buildozer.spec ]; then
        echo "📝 Initializing buildozer configuration..."
        buildozer init -f
    else
        echo "✅ buildozer.spec already exists, skipping init"
    fi
fi

echo "✨ Setup complete! You can now:"
echo "  - Build APK: cd mobile && buildozer -v android debug"
echo "  - View logs: .buildozer/android/platform/build/logs"
