from mitmproxy import http, ctx, proxy, options
from mitmproxy.tools.dump import DumpMaster
import https_everywhere_standalone_pyo as https_everywhere
import os, sys, argparse
from ipaddress import ip_address
from pathlib import Path
import web_ui

parser = argparse.ArgumentParser()
parser.add_argument('--transparent', action='store_true', default=False,
        help='Run in transparent mode (default: false)')
parser.add_argument('--host', dest='proxy_host', type=ip_address, default='127.0.0.1',
        help='Host to run proxy on (default: 127.0.0.1)')
parser.add_argument('--port', dest='proxy_port', type=int, default=8080,
        help='Port to run proxy on (default: 8080)')
parser.add_argument('--web-ui-host', dest='web_ui_host', type=ip_address, default='127.0.0.1',
        help='Host to run web ui on (default: 127.0.0.1)')
parser.add_argument('--web-ui-port', dest='web_ui_port', type=int, default=8081,
        help='Port to run web ui on (default: 8081)')
args = parser.parse_args()


class Rewriter:
    def __init__(self):
        initial_path = os.getcwd()

        os.chdir(Path.home())

        self.rs_ptr = https_everywhere.create_rulesets()
        self.s_ptr = https_everywhere.create_storage()
        self.settings_ptr = https_everywhere.create_settings(self.s_ptr)
        self.rw_ptr = https_everywhere.create_rewriter(self.rs_ptr, self.settings_ptr)

        # If we are packaged as a standalone executable, cd into temp dir
        # otherwise, cd to initial path
        try:
            os.chdir(sys._MEIPASS)
        except AttributeError:
            os.chdir(initial_path)

        self.updater_ptr = https_everywhere.create_updater(self.rs_ptr, self.s_ptr)
        https_everywhere.update_rulesets(self.updater_ptr)

    def update(self, updates):
        if "ease" in updates:
            https_everywhere.set_ease_mode_enabled(self.settings_ptr, updates['ease'])
        if "enabled" in updates:
            https_everywhere.set_enabled(self.settings_ptr, updates['enabled'])

    def set_site_disabled(self, site, disabled):
        return https_everywhere.set_site_disabled(self.settings_ptr, site, disabled)

    def settings(self):
        return {'ease': https_everywhere.get_ease_mode_enabled_or(self.settings_ptr, False),
                'enabled': https_everywhere.get_enabled_or(self.settings_ptr, True),
                'update_channel_timestamps': https_everywhere.get_update_channel_timestamps(self.updater_ptr),
                'sites_disabled': https_everywhere.get_sites_disabled(self.settings_ptr),
               }

    def request(self, flow):
        url = flow.request.pretty_url
        ra = https_everywhere.rewrite_url(self.rw_ptr, url)
        if ra[0] == True:
            flow.response = http.HTTPResponse.make(
                302,
                b"HTTPS Everywhere has blocked this request",
                {"Content-Type": "text/html", "Location": "https" + url[4:]}
            )
            ctx.log.debug("Cancelling request for: \n\t" + url)
        elif ra[1] == True:
            ctx.log.debug("Not modifying request for: \n\t" + url)
            pass
        elif ra[3] == True:
            flow.response = http.HTTPResponse.make(
                409,
                b"HTTPS Everywhere is attempting to upgrade this connection, but the website is downgrading it to HTTP.  This is causing a redirection loop.  To access this site, please change your settings to exclude this domain from HTTPS Everywhere and refresh this page.",
            )
            ctx.log.debug("Responding with redirect warning for: \n\t" + url)
        else:
            ctx.log.debug("Redirecting request for/to: \n\t" + url + "\n\t" + ra[2])
            flow.response = http.HTTPResponse.make(
                302,
                b"HTTPS Everywhere has blocked this request",
                {"Location": ra[2]}
            )


    def __del__(self):
        https_everywhere.destroy_updater(self.updater_ptr)
        https_everywhere.destroy_rewriter(self.rw_ptr)
        https_everywhere.destroy_settings(self.settings_ptr)
        https_everywhere.destroy_storage(self.s_ptr)
        https_everywhere.destroy_rulesets(self.rs_ptr)


rw = Rewriter()

opts = options.Options(listen_host=str(args.proxy_host), listen_port=args.proxy_port)
opts.add_option("body_size_limit", int, 0, "")
opts.add_option("allow_hosts", list, ["^http:"], "")
opts.add_option("dumper_filter", str, "error", "")
if args.transparent:
    opts.add_option("mode", str, "transparent", "")
pconf = proxy.config.ProxyConfig(opts)

m = DumpMaster({}, with_dumper=False)
m.addons.add(rw)
m.server = proxy.server.ProxyServer(pconf)

try:
        web_ui.run(args.web_ui_host, args.web_ui_port, rw)
        m.run()
except KeyboardInterrupt:
        m.shutdown()
        web_ui.shutdown()