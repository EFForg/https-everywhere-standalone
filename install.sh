#!/bin/bash

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

if wget -c -P rust/wheels/ https://github.com/EFForg/https-everywhere-mitmproxy-wheels/raw/master/https_everywhere_mitmproxy_pyo-0.1.0-${IMPLEMENTATION}${VERSION}-${IMPLEMENTATION}${MVER}-${PLATFORM}_${ARCH}.whl; then
	pip3 install -r requirements.txt
	pip3 install --upgrade --force pyasn1 # who knows why we have to do this...
	echo "Are you installing on a workstation or a router?"
	select wr in workstation router; do
		case $wr in
			workstation ) echo "Adding user 'httpse'..."
				useradd -rmu 1789 -d /var/lib/httpse httpse
				echo "Creating 'pre-mitm.sh'..."
				echo "iptables -t nat -A OUTPUT -p tcp --dport 80 -m owner ! --uid-owner 1789 -j DNAT --to 127.0.0.1:8080" > pre-mitm.sh
				chmod +x pre-mitm.sh
				echo "Creating 'post-mitm.sh'..."
				echo "iptables -t nat -D OUTPUT -p tcp --dport 80 -m owner ! --uid-owner 1789 -j DNAT --to 127.0.0.1:8080" > post-mitm.sh
				chmod +x post-mitm.sh
				echo "Altering 'mitm.sh' to run from new 'httpse' user..."
				sed -i 's/^python/sudo -u httpse python/g' mitm.sh
				echo "DONE"
				break
				;;
			router ) cp pre-mitm.sh.example pre-mitm.sh
				cp post-mitm.sh.example post-mitm.sh
				echo "Alter the iptables rules in 'pre-mitm.sh' and 'post-mitm.sh' to reflect your own network setup."
				echo "DONE"
				break
				;;
			* ) echo "Please select a valid option."
				;;
		esac
	done
else
	echo "Error: https-everywhere-mitmproxy is not supported on your system."
fi
