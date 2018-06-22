/* eslint-disable */
'use strict'
/* Angular JQuery Sync */
/**
 * Get cookies by name.
 * @function getCookie
 * @param {string} name Cookie name
 * @return {null|string} Return the cookies of a previous session
 */
const getCookie = function getCookie (name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cont = 0; cont < cookies.length; cont++) {
      const cookie = jQuery.trim(cookies[cont]);
      if (cookie.substring(0, name.length + 1) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

/**
 * Verify the send method of cookie request.
 * @function csrfSafeMethod
 * @param {String} method Request method for get cookies
 * @return {boolean} Return boolean if request method is valid
 */
const csrfSafeMethod = function csrfSafeMethod (method) {
  return (/^(GET|HEAD|OPTIONS)$/).test(method);
};

/**
 * Verify if the url is in Integrates domain.
 * @function sameOrigin
 * @param {string} url User actual url
 * @return {boolean} Boolean response if user actual url is valid
 */
const sameOrigin = function sameOrigin (url) {
  const hostOrigin = document.location.host;
  const protocolOrigin = document.location.protocol;
  const srOrigin = `//${hostOrigin}`;
  const origin = protocolOrigin + srOrigin;
  return url === origin || url.slice(0, origin.length + 1) === `${origin}/` ||
        (url === srOrigin || url.slice(0, srOrigin.length + 1) ===
        `${srOrigin}/`) || !(/^(\/\/|http:|https:).*/).test(url);
};
/**
 * Add the CSRF cookie to all ajax requests.
 * @function ajaxConfig
 * @return {undefined}
 */
const ajaxConfig = function ajaxConfig () {
  $.ajaxSetup({
    "beforeSend" (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        const csrftoken = getCookie("csrftoken");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
};
/**
 * Add the CSRF cookie to all ajax requests.
 * @function ajaxConfig
 * @return {undefined}
 */
var $xhr = new class xhr {
  request($method, $q, $url, $data, text){
    var deferred = $q.defer();
    try {
      if(!$q) throw "Undefined Promise";
      if(!$url) throw "Undefined URL";
      $.ajax({
        url: $url, type: $method, data: $data,
        success: function (response) { 
          deferred.resolve(response); 
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
          if(XMLHttpRequest.status == 401){
            location = BASE.url + "index";
          }else{
            throw text;
          }
        }
      });
    } catch (e) {
      Rollbar.error(text);
      let textError = (localStorage.lang === 'es')
        ?"Hay un error"
        :"There is an error";
      $.gritter.add({ 
          title: 'Oops!', text: textError,
          class_name: 'color warning', sticky: false,
      });
      deferred.resolve(e);
    }
    return deferred.promise;
  }
  get($q, $url, $data, text = {}){ return this.request("get", $q, $url, $data, text) }
  post($q, $url, $data, text = {}){ return this.request("post", $q, $url, $data, text) }
  fetch($q, $data, text = {}){
    return this.request("post", $q, BASE.url + "api", $data, text);
  }
};
//Run ajax config
ajaxConfig();
//Overriding ajax
$("#full_loader").hide();
$( document ).ajaxStart(function() { $("#full_loader").show(); });
$( document ).ajaxStop(function() { $("#full_loader").hide(); });
$( document ).ajaxError(function() { $("#full_loader").hide(); });
