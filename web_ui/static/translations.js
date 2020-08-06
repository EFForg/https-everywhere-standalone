let get_translator = () => {
  return new Promise(resolve => {
    var request = new XMLHttpRequest();
    request.open('get', '/static/messages.json');
    request.responseType = 'json';
    request.send();

    request.onload = function() {
      request.response['en'] = request.response['templates'];
      let translate = key => {
        for(language of navigator.languages) {
          if(language in request.response && key in request.response[language]){
            return request.response[language][key];
          }
        }
        return request.response['templates'][key];
      }
      resolve(translate);
    }
  });
}
