// This file should not be renamed.
/* eslint-disable angular/file-name */
// This file is an Angular configuration script for Integrates services
/* eslint-disable angular/component-limit*/
// Angular module configuration only can be made with parameter array injection.
/* eslint angular/di: [2,"array"] */
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
 * Set main route for ajax requests.
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
$msg.warning = function warning (text, title) {
  $.gritter.add({
    "class_name": "color warning",
    "sticky": false,
    text,
    title
  });
};

/**
 * Set Integrates as an Angular app.
 * @module {AngularJS} FluidIntegrates
 */
angular.module("FluidIntegrates", [
  "ngSanitize",
  "betsol.intlTelInput",
  "monospaced.elastic",
  "ngNotify",
  "pascalprecht.translate",
  "tandibar/ng-rollbar",
  "ui.bootstrap",
  "ui.router"
]);
angular.module("FluidIntegrates").config([
  "RollbarProvider",
  function initRollbar (RollbarProvider) {
    const isProduction = location.toString().indexOf("localhost:8000") === -1;
    let fiEnvironment = "production";
    if (location.toString().
      indexOf(".integrates.env.fluidattacks.com") !== -1) {
      fiEnvironment = "review";
    }
    RollbarProvider.init({
      "accessToken": "cad6d1f7ecda480ba003e29f0428d44e",
      "captureUncaught": true,
      "enabled": isProduction,
      "payload": {"environment": fiEnvironment}
    });
  }
]);
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

/*
 * Ignoring exception in template load failures
 *
 * This exception is going to happen during deploy
 * downtime. If an user attempts to browse into
 * application right in the deployment.
 *
 * Disabling here is necessary because the error
 * isn't a fixable issue, unless
 * we achieve a zero-downtime deploy
 */
angular.module("FluidIntegrates").config([
  "$provide",
  function config ($provide) {
    $provide.decorator("$templateRequest", [
      "$delegate",
      function catchRequest ($delegate) {
        const callFn = function callFn (template) {
          return $delegate(template, true);
        };
        return callFn;
      }
    ]);
  }
]);
