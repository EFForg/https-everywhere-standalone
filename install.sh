#!/bin/bash

PLATFORM=`python3 -c "import sys; print(sys.platform.lower())"`
ARCH=`python3 -c "import platform; print(platform.machine().lower())"`
VERSION=`python3 -c "import version; print(version.VERSION_STRING)"`
if [ "$PLATFORM" == "win32" ]; then
	EXTENSION=".exe"
fi

if wget -c -O dist/https-everywhere-standalone${EXTENSION} https://github.com/EFForg/https-everywhere-standalone/releases/download/v${VERSION}/https-everywhere-standalone-${VERSION}-${PLATFORM}-${ARCH}${EXTENSION}; then
	if [ "$PLATFORM" == "win32" ]; then
	  echo "Installing as a transparent proxy on windows is not supported at this time.  You can run this as an HTTP proxy, the executable is in the 'dist' folder."
	  exit 1
	fi
	chmod +x dist/https-everywhere-standalone${EXTENSION}
	echo "Are you installing on a workstation or a router?"
	select wr in workstation router; do
		case $wr in
			workstation ) if [ $UID != "0" ]; then
				  echo "This script must be run as root to install on a workstation"
				  exit 1
				fi
				echo "Adding user 'httpse'..."
				useradd -rmu 1789 -d /var/lib/httpse httpse
				echo "Creating 'pre-mitm.sh'..."
				echo "iptables -t nat -A OUTPUT -p tcp --dport 80 -m owner ! --uid-owner 1789 -j DNAT --to 127.0.0.1:8080" > pre-mitm.sh
				chmod +x pre-mitm.sh
				echo "Creating 'post-mitm.sh'..."
				echo "iptables -t nat -D OUTPUT -p tcp --dport 80 -m owner ! --uid-owner 1789 -j DNAT --to 127.0.0.1:8080" > post-mitm.sh
				chmod +x post-mitm.sh
				echo "Moving binary to 'httpse' home directory..."
				chown httpse:httpse dist/https-everywhere-standalone${EXTENSION}
				mv dist/https-everywhere-standalone${EXTENSION} /var/lib/httpse/
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
	echo "Error: https-everywhere-standalone is not supported on your system."
fi
