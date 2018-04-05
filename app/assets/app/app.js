/* eslint no-magic-numbers: ["error", { "ignore": [1, -1, 0] }]*/
/* global document, jQuery, $, location, angular, isProduction:true */
/**
 * @file app.js
 * @author engineering@fluidattacks.com
 */
/**
 * Obtiene una cookie atraves de su nombre
 * @function getCookie
 * @param {String} name
 * @return {String}
 */
function getCookie (name) {
  let cookieValue = null;
  if (document.cookie && document.cookie != "") {
    const cookies = document.cookie.split(";");
    for (let cont = 0; cont < cookies.length; cont++) {
      const cookie = jQuery.trim(cookies[cont]);
      if (cookie.substring(0, name.length + 1) == `${name}=`) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/**
 * Verifica el metodo por el cual se va a enviar una peticion de cookie
 * @function csrfSafeMethod
 * @param {String} method
 * @return {Boolean}
 */
function csrfSafeMethod (method) {
  return (/^(GET|HEAD|OPTIONS)$/).test(method);
}

/**
 * Verifica si la url dada esta dentro del mismo dominio
 * @function sameOrigin
 * @param {String} url
 * @return {Boolean}
 */
function sameOrigin (url) {
  const host = document.location.host;
  const protocol = document.location.protocol;
  const sr_origin = `//${host}`;
  const origin = protocol + sr_origin;
  return url == origin || url.slice(0, origin.length + 1) == `${origin}/` ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == `${sr_origin}/`) ||
        !(/^(\/\/|http:|https:).*/).test(url);
}

/**
 * Agrega la cookie de CSRF a todas las peticiones ajax de la aplicacion
 * @function ajaxConfig
 * @return {undefined}
 */
function ajaxConfig () {
  $.ajaxSetup({
    "beforeSend" (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        const csrftoken = getCookie("csrftoken");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
}

/*
 * Establece la ruta principal para las peticiones ajax
 */
const BASE = {
  "development": "/",
  "production": "/integrates/"
};
BASE.url = BASE.production;
if (location.pathname.indexOf("/integrates") == -1) {
  BASE.url = BASE.development;
}
const $msg = {};
$msg.success = function (text, title) {
  $.gritter.add({
    "class_name": "color info",
    "sticky": false,
    text,
    title
  });
};
$msg.error = function (text, title = "Oops!") {
  $.gritter.add({
    "class_name": "color danger",
    "sticky": false,
    text,
    title
  });
};
$msg.info = function (text, title) {
  $.gritter.add({
    "class_name": "color info",
    "sticky": false,
    text,
    title
  });
};
$msg.warning = function (text, title) {
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
  function (RollbarProvider) {
    isProduction = location.toString().indexOf("localhost:8000") == -1;
    RollbarProvider.init({
      "accessToken": "cad6d1f7ecda480ba003e29f0428d44e",
      "captureUncaught": true,
      "enabled": isProduction,
      "payload": {"environment": "production"}
    });
  }
]);
