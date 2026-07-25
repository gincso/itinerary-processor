
[app]

# (str) Title of your application
title = Itinerary Driver

# (str) Package name
package.name = itinerarydriver

# (str) Package domain (needed for android/ios packaging)
package.domain = org.agentzero

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to ignore (let empty to not ignore anything)
#source.exclude_exts = spec

# (list) List of directory to ignore (let empty to not ignore anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
requirements = python3,kivy,requests,kivy_garden.mapview

# (str) Custom source folders for requirements
# requirements.source = 

# (list) Garden requirements
# garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PYTHON_FILE

# (str) OSX Specific: The NSPrincipalClass of your application
# osx.principal_class = Python

# (str) OSX Specific: The NSHighResolutionCapable property of your application
# osx.highresolution_capable = 1

# (str) Android specific: the Android SDK to use
#android.sdk = /path/to/android/sdk

# (str) Android specific: the Android NDK to use
#android.ndk = /path/to/android/ndk

# (int) Android specific: the Android API to target
android.api = 30

# (int) Android specific: the minimum Android API required
android.minapi = 21

# (int) Android specific: the Android NDK version to use
#android.ndk_api = 21

# (bool) Android specific: if true, skip Java compilation step
#android.skip_compile_java = False

# (list) Android specific: the Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Android specific: automatically accept SDK licenses
android.accept_sdk_license = True
