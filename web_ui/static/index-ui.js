let ease, enabled, ease_label, enabled_label, t;

window.onload = async () => {
  t = await get_translator();
  ease = document.getElementById('ease');
  ease_label = document.getElementById('ease_label');
  enabled = document.getElementById('enabled');
  enabled_label = document.getElementById('enabled_label');

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
