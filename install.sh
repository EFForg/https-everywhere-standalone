PLATFORM=`python3 -c "import sys; print(sys.platform)"`
ARCH=`python3 -c "import platform; print(platform.machine())"`
VERSION=`python3 -c "import platform; print(platform.python_version()[:3])" | sed 's/\.//g'`
ARCH=`python3 -c "import platform; print(platform.machine())"`
IMPLEMENTATION=`python3 -c "import platform; print(platform.python_implementation())"`
if [ "$IMPLEMENTATION" == "CPython" ]; then
	IMPLEMENTATION=cp
fi
if [ "$VERSION" == "38" ]; then
	MVER=38
else
	MVER=${VERSION}m
fi

if wget -P rust/wheels/ https_everywhere_mitmproxy_pyo-0.1.0-${IMPLEMENTATION}${VERSION}-${IMPLEMENTATION}${MVER}-${PLATFORM}_${ARCH}.whl; then
	pip3 install -r requirements.txt
else
	echo "Error: https-everywhere-mitmproxy is not supported on your system."
fi
