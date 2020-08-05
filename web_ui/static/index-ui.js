let ease;

window.onload = () => {
  ease = document.getElementById('ease');
  ease.onchange = () => {
    send_settings({'ease': ease.checked});
  }
  enabled = document.getElementById('enabled');
  enabled.onchange = () => {
    send_settings({'enabled': enabled.checked});
  }

  let rulesets_versions = document.getElementById('rulesets-versions');

  rulesets_versions.addSpan = function(update_channel_name, ruleset_version_string) {
    let timestamp_span = document.createElement("span");
    timestamp_span.className = "rulesets-version";
    timestamp_span.innerText = `Rulesets version for ${update_channel_name}: ${ruleset_version_string}`;
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
}

function send_settings(changed_settings) {
  console.log(ease.checked);
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() {
    if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
      console.log(xmlHttp.responseText);
    }
  }
  xmlHttp.open("post", "settings_changed"); 
  xmlHttp.send(JSON.stringify(changed_settings)); 
}
