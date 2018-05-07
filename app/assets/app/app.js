/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global
document, jQuery, $, location, angular, isProduction:true,
translations1, traducciones1, translations2, traducciones2
*/
/**
 * @file app.js
 * @author engineering@fluidattacks.com
 */
/**
 * Obtiene una cookie a traves de su nombre
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
 * Verifica el metodo por el cual se va a enviar una peticion de cookie
 * @function csrfSafeMethod
 * @param {String} method Request method for get cookies
 * @return {boolean} Return boolean if request method is valid
 */
const csrfSafeMethod = function csrfSafeMethod (method) {
  return (/^(GET|HEAD|OPTIONS)$/).test(method);
};

/**
 * Verifica si la url dada esta dentro del mismo dominio
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
 * Agrega la cookie de CSRF a todas las peticiones ajax de la aplicacion
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

/*
 * Establece la ruta principal para las peticiones ajax
 */
const BASE = {
  "development": "/",
  "production": "/integrates/"
};
BASE.url = BASE.production;
if (location.pathname.indexOf("/integrates") === -1) {
  BASE.url = BASE.development;
}
const $msg = {};
$msg.success = function success (text, title) {
  $.gritter.add({
    "class_name": "color info",
    "sticky": false,
    text,
    title
  });
};
$msg.error = function error (text, title = "Oops!") {
  $.gritter.add({
    "class_name": "color danger",
    "sticky": false,
    text,
    title
  });
};
$msg.info = function info (text, title) {
  $.gritter.add({
    "class_name": "color info",
    "sticky": false,
    text,
    title
  });
};
$msg.warning = function warning (text, title) {
  $.gritter.add({
    "class_name": "color warning",
    "sticky": false,
    text,
    title
  });
};

/**
 * Crea integrates como una aplicacion de angular
 * @module {AngularJS} FluidIntegrates
 */
const integrates = angular.module("FluidIntegrates", [
  "ui.router",
  "ui.bootstrap",
  "pascalprecht.translate",
  "ngSanitize",
  "ngNotify",
  "prismjsHighlight",
  "monospaced.elastic",
  "tandibar/ng-rollbar"
]);
integrates.config([
  "RollbarProvider",
  function initRollbar (RollbarProvider) {
    const isProduction = location.toString().indexOf("localhost:8000") === -1;
    RollbarProvider.init({
      "accessToken": "cad6d1f7ecda480ba003e29f0428d44e",
      "captureUncaught": true,
      "enabled": isProduction,
      "payload": {"environment": "production"}
    });
  }
]);

/**
 * Establece la configuracion de las traducciones de integrates
 * @name config
 * @config {AngularJS}
 * @param {Object} $translateProvider Angular translator dependecy
 * @return {undefined}
 */
integrates.config([
  "$translateProvider",
  function config ($translateProvider) {
    $translateProvider.useSanitizeValueStrategy("sanitizeParameters");
    if (typeof localStorage.lang === "undefined") {
      localStorage.lang = "en";
    }
    $translateProvider.
      translations("en", translations1).
      translations("en", translations2).
      translations("es", traducciones1).
      translations("es", traducciones2).
      preferredLanguage(localStorage.lang);
  }
]);
