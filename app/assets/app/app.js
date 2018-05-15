/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global
document, jQuery, $, location, angular, isProduction:true,
translations1, traducciones1, translations2, traducciones2
*/
/**
 * @file app.js
 * @author engineering@fluidattacks.com
 */
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
angular.module("FluidIntegrates", [
  "ngSanitize",
  "monospaced.elastic",
  "ngNotify",
  "pascalprecht.translate",
  "prismjsHighlight",
  "tandibar/ng-rollbar",
  "ui.bootstrap",
  "ui.router"
]);
angular.module("FluidIntegrates").config([
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
angular.module("FluidIntegrates").config([
  "$translateProvider",
  function config ($translateProvider) {
    $translateProvider.useSanitizeValueStrategy("sanitizeParameters");
    if (angular.isUndefined(localStorage.lang)) {
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
