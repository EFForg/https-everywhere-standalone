# HTTPS Everywhere Standalone

[HTTPS Everywhere](https://www.eff.org/https-everywhere) is a project which seeks to standardize usage of the secure HTTPS transport layer over antiquated HTTP.  HTTPS Everywhere maintains a list of sites that support HTTPS, and redirects requests if a user attempts to visit HTTP using a browser addon.

HTTPS Everywhere Standalone seeks to achieve this same goal by providing a proxy which can be configured in the browser or operating system.  HTTPS Everywhere Standalone can act as either an HTTP or transparent proxy.

## How it works

We owe much of the functionality of this project to [`mitmproxy`](https://mitmproxy.org/), which has a robust plugin architecture that allows python scripts to read and modify HTTP headers.  It can act as a transparent proxy, allowing real-time interception of web traffic.  Here, we are using the capabilities of `mitmproxy` in combinaion with HTTPS Everywhere to spoof web headers delivered over HTTP to forward users to HTTPS transparently.  Any device which is being intercepted by `mitmproxy` (for instance, by setting up a Raspberry Pi MitM access point using [RaspberryPi-Packet-Sniffer](https://github.com/Hainish/RaspberryPi-Packet-Sniffer) and having devices connect to it) will automatically have its traffic secured via HTTPS Everywhere.

This project uses the [`https-everywhere-lib-core`](https://github.com/EFForg/https-everywhere-lib-core/) rust library, providing rust bindings to the python plugin code.

## Using

Platform support is limited, so first try this.  If it doesn't work, try the 'developing' section below.

    sudo apt install libssl-dev locales-all python3-pip wget
    sudo ./install.sh
    sudo ./mitm.sh

## Developing

In order to build the project, you'll need to have [rust](https://rust-lang.org/) >= 1.39 installed.

    sudo apt install libssl-dev pkg-config python3-pip python3-venv libsqlite3-dev
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
    cd rust
    git submodule update --init
    maturin develop --release   # this build step will take a while
    cd ..
    cp pre-mitm.sh.example pre-mitm.sh     # edit this file if necessary, this is meant to work with the above RasPi project
    cp post-mitm.sh.example post-mitm.sh   # same here
    sudo ./mitm.sh
