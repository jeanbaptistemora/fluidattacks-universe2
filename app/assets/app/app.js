// This file should not be renamed.
/* eslint-disable angular/file-name */
// This file is an Angular configuration script for Integrates services
/* eslint-disable angular/component-limit*/
// Angular module configuration only can be made with parameter array injection.
/* eslint angular/di: [2,"array"] */
/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* eslint-disable angular/window-service */
/* global
document, jQuery, $, location, angular, isProduction:true,
translations1, traducciones1, Rollbar
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
/**
 * Set Integrates as an Angular app.
 * @module {AngularJS} FluidIntegrates
 */
angular.module("FluidIntegrates", [
  "ui.router"
]);
