Please note that this is a research project for testing the viability of this solution. Because of this we can't commit to maintain, introduce new features, nor fix bugs.

# HTTPS Everywhere Standalone

[HTTPS Everywhere](https://www.eff.org/https-everywhere) is a project which seeks to standardize usage of the secure HTTPS transport layer over antiquated HTTP.  HTTPS Everywhere maintains a list of sites that support HTTPS, and redirects requests if a user attempts to visit HTTP using a browser addon.

HTTPS Everywhere Standalone seeks to achieve this same goal by providing a proxy which can be configured in the browser or operating system.  HTTPS Everywhere Standalone can act as either an HTTP or transparent proxy.

## How it works

We owe much of the functionality of this project to [`mitmproxy`](https://mitmproxy.org/), which has a robust plugin architecture that allows python scripts to read and modify HTTP headers.  It can act as a transparent proxy, allowing real-time interception of web traffic.  Here, we are using the capabilities of `mitmproxy` in combinaion with HTTPS Everywhere to spoof web headers delivered over HTTP to forward users to HTTPS transparently.  Any device which is being intercepted by `mitmproxy` (for instance, by setting up a Raspberry Pi MitM access point using [RaspberryPi-Packet-Sniffer](https://github.com/Hainish/RaspberryPi-Packet-Sniffer) and having devices connect to it) will automatically have its traffic secured via HTTPS Everywhere.

This project uses the [`https-everywhere-lib-core`](https://github.com/EFForg/https-everywhere-lib-core/) rust library, providing rust bindings to the python plugin code.

## Using

Platform support is limited, so first try this.  If it doesn't work, try the 'developing' section below.

    sudo apt install libssl-dev locales-all wget
    sudo ./install.sh
    sudo ./mitm.sh

## Developing

### Setup

In order to build the project, you'll need to have [rust](https://rust-lang.org/) >= 1.48 and [pipenv](https://pypi.org/project/pipenv/) >= 2020.11.15 installed.

#### Debian Linux

    sudo apt install libssl-dev pkg-config python3-pip libffi-dev libjpeg-dev libsqlite3-dev
    pipenv --python 3.7
    pipenv install
    cd rust
    git submodule update --init
    pipenv run maturin develop --release   # this build step will take a while
    cd ..
    cp pre-mitm.sh.example pre-mitm.sh     # edit this file if necessary, this is meant to work with the above RasPi project
    cp post-mitm.sh.example post-mitm.sh   # same here

#### Windows 10

Ensure you've installed python 3.7 from the python website, and not the Windows Store.  Then,

    C:\path\to\vcpkg.exe install openssl:x64-windows-static-md sqlite3:x64-windows-static-md
    py -m pipenv --python 3.7
    py -m pipenv install
    cd rust
    py -m pipenv run maturin develop --release

### Running

    ./pre-mitm.sh
    pipenv run python https-everywhere-standalone.py
    ./post-mitm.sh

## Building (Reproducible)

A bit-by-bit reproducible build can be generated.

## Debian Linux

To verify our Linux builds, the repository must be owned by a user named `user` and live in `/home/user/workspace/https-everywhere-standalone`.

First, following the steps above in [Setup](#Setup).  Then running the following:

    PYTHONHASHSEED=1
    export PYTHONHASHSEED
    pipenv run pyinstaller --clean https-everywhere-standalone.spec
    sha256sum dist/https-everywhere-standalone

## Windows 10

To verify our Windows build, the repository must be owned by a user named `User` and live in `C:\Users\User\workspace\https-everywhere-standalone`.

First, follow the steps above in [Setup](#Setup), modifying for Windows.  Then run the following using Powershell:

    py -m pipenv shell
    $env:PYTHONHASHSEED=1
    pyinstaller --clean https-everywhere-standalone.spec
