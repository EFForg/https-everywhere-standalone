from mitmproxy import http, ctx, proxy, options
from mitmproxy.tools.dump import DumpMaster
import https_everywhere_mitmproxy_pyo as https_everywhere
import os, sys, argparse

class Rewriter:
    def __init__(self):
        initial_path = os.getcwd()

        os.chdir(Path.home())

        self.rs_ptr = https_everywhere.create_rulesets()
        self.s_ptr = https_everywhere.create_storage()
        self.rw_ptr = https_everywhere.create_rewriter(self.rs_ptr, self.s_ptr)
        self.settings_ptr = https_everywhere.create_settings(self.s_ptr)

        # If we are packaged as a standalone executable, cd into temp dir
        # otherwise, cd to initial path
        try:
            os.chdir(sys._MEIPASS)
        except AttributeError:
            os.chdir(initial_path)

        https_everywhere.update_rulesets(self.rs_ptr, self.s_ptr)

    def load(self, loader):
        loader.add_option(
            name = "https_everywhere_enabled",
            typespec = bool,
            default = True,
            help = "Enable or disable HTTPS Everywhere",
        )
        loader.add_option(
            name = "https_everywhere_ease_mode",
            typespec = bool,
            default = False,
            help = "Enable or disable HTTPS Everywhere's Encrypt All Sites Eligible (EASE) mode.  This disallows HTTP requests from going through.",
        )

    def configure(self, updates):
        if "https_everywhere_enabled" in updates:
            value = ctx.options.https_everywhere_enabled
            if value is not None:
                https_everywhere.set_enabled(self.settings_ptr, value)
        if "https_everywhere_ease_mode" in updates:
            value = ctx.options.https_everywhere_ease_mode
            if value is not None:
                https_everywhere.set_ease_mode_enabled(self.settings_ptr, value)

    def request(self, flow):
        url = flow.request.pretty_url
        ra = https_everywhere.rewrite_url(self.rw_ptr, url)
        if ra[0] == True:
            flow.response = http.HTTPResponse.make(
                302,
                b"HTTPS Everywhere has blocked this request",
                {"Content-Type": "text/html", "Location": "https" + url[4:]}
            )
            ctx.log.info("Cancelling request for: \n\t" + url)
        elif ra[1] == True:
            ctx.log.info("Not modifying request for: \n\t" + url)
            pass
        else:
            ctx.log.info("Redirecting request for/to: \n\t" + url + "\n\t" + ra[2])
            flow.response = http.HTTPResponse.make(
                302,
                b"HTTPS Everywhere has blocked this request",
                {"Location": ra[2]}
            )


    def __del__(self):
        https_everywhere.destroy_rewriter(self.rw_ptr)
        https_everywhere.destroy_settings(self.settings_ptr)
        https_everywhere.destroy_rulesets(self.rs_ptr)
        https_everywhere.destroy_storage(self.s_ptr)


parser = argparse.ArgumentParser()
parser.add_argument('--transparent', action='store_true', default=False,
        help='Run in transparent mode (default: false)')
args = parser.parse_args()

opts = options.Options(listen_host='127.0.0.1', listen_port=8080)
opts.add_option("body_size_limit", int, 0, "")
opts.add_option("allow_hosts", list, ["^http"], "")
opts.add_option("flow_detail", int, 0, "")
opts.add_option("termlog_verbosity", str, "error", "")
if args.transparent:
    opts.add_option("mode", str, "transparent", "")
pconf = proxy.config.ProxyConfig(opts)

m = DumpMaster(None)
m.addons.add(Rewriter())
m.server = proxy.server.ProxyServer(pconf)

try:
        m.run()
except KeyboardInterrupt:
        m.shutdown()
