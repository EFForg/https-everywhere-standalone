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
