let ease, enabled, ease_label, enabled_label, t, sites_disabled_wrapper;

window.onload = async () => {
  t = await get_translator();
  ease = document.getElementById('ease');
  ease_label = document.getElementById('ease_label');
  enabled = document.getElementById('enabled');
  enabled_label = document.getElementById('enabled_label');
  sites_disabled_wrapper = document.getElementById('sites_disabled_wrapper');

  ease.onchange = () => {
    send_settings({'ease': ease.checked});
    update_ui();
  }
  enabled.onchange = () => {
    send_settings({'enabled': enabled.checked});
    update_ui();
  }

  let rulesets_versions = document.getElementById('rulesets-versions');

  rulesets_versions.addSpan = function(update_channel_name, ruleset_version_string) {
    let timestamp_span = document.createElement("span");
    timestamp_span.className = "rulesets-version";
    timestamp_span.innerText = `${t("about_rulesets_version")} ${update_channel_name}: ${ruleset_version_string}`;
    this.appendChild(timestamp_span);
  };

  for(let name in update_channel_timestamps) {
    let timestamp = update_channel_timestamps[name];
    if(timestamp > 0) {
      let ruleset_date = new Date(timestamp * 1000);
      let ruleset_version_string = ruleset_date.getUTCFullYear() + "." + (ruleset_date.getUTCMonth() + 1) + "." + ruleset_date.getUTCDate();

      rulesets_versions.addSpan(name, ruleset_version_string);
    }
  }

  // img element "remove button"
  let template_remove = document.createElement("img");
  template_remove.src = "/static/images/remove.png";
  template_remove.className = "remove";

  while(sites_disabled_wrapper.hasChildNodes()) {
    sites_disabled_wrapper.removeChild(sites_disabled_wrapper.lastChild);
  }
  function add_site_disabled(key) {
    let site_div = document.createElement("div");
    let remove = template_remove.cloneNode(true);
    let site_name = document.createElement("p");

    site_div.className = "site-disabled-list-item";
    site_name.className = "site-diabled-item_single";
    site_name.innerText = key;
    site_div.appendChild( site_name);
    site_div.appendChild(remove);
    sites_disabled_wrapper.appendChild(site_div);

    remove.addEventListener("click", () => {
      sites_disabled_wrapper.removeChild(site_div);
      set_site_disabled(key, false);
    });
  }

  for (const key of sites_disabled) {
    add_site_disabled(key);
  }

  const sites_disabled_header = document.getElementById("sites_disabled_header");
  const add_site_disabled_button = document.getElementById("add_site_disabled");
  const site_disabled_input = document.getElementById("site_disabled");
  sites_disabled_header.innerText = t("options_disabledUrlsListed");
  site_disabled_input.setAttribute("placeholder", t("options_enterDisabledSite"));
  add_site_disabled_button.innerText = t("options_addDisabledSite");

  add_site_disabled_button.addEventListener("click", async function() {
    const success = await set_site_disabled(site_disabled_input.value, true);
    if (success) {
      add_site_disabled(site_disabled_input.value);
    } else {
      t("options_hostNotFormattedCorrectly");
    }
  });


  update_ui();
}

function send_settings(changed_settings) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() {
    if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
      console.log(xmlHttp.responseText);
    }
  }
  xmlHttp.open("post", "/settings_changed");
  xmlHttp.send(JSON.stringify(changed_settings)); 
}

function set_site_disabled(site, disabled) {
  return new Promise(resolve => {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
      if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
        console.log(xmlHttp.responseText);
        resolve(xmlHttp.responseText === 'true');
      }
    }
    xmlHttp.open("post", "/set_site_disabled");
    xmlHttp.send(JSON.stringify({site, disabled}));
  });
}

function update_ui() {
  if(enabled.checked) {
    enabled_label.innerText = t("menu_globalEnable");
  } else {
    enabled_label.innerText = t("menu_globalDisable");
  }

  if(ease.checked) {
    ease_label.innerText = t("menu_encryptAllSitesEligibleOn");
  } else {
    ease_label.innerText = t("menu_encryptAllSitesEligibleOff");
  }

}
