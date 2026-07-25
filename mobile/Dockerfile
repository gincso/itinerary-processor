
FROM beevelop/android:2026.5.9

# Install Buildozer dependencies
RUN apt update && apt install -y     python3-pip     autoconf     automake     libtool     pkg-config     zlib1g-dev     libncurses-dev     cmake     libffi-dev     libssl-dev

# Fix libtool macro compatibility for libffi
RUN echo "AC_DEFUN([LT_SYS_SYMBOL_USCORE], [AC_CHECK_LIB([c], [main], [], [])])" > /usr/share/aclocal/libtool-uscore.m4

# Install Buildozer
RUN pip install --user buildozer python-for-android

# Set up working directory
WORKDIR /app

# Copy mobile app files
COPY . .

# Build command
CMD ["buildozer", "-v", "android", "debug"]
