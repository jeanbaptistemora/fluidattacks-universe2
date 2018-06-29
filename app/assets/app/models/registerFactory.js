/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1, 5] }]*/
/* global integrates, BASE, $xhr, $, Rollbar,
angular, secureRandom */
/**
 * @file registerFactory.js
 * @author engineering@fluidattacks.com
 */
/**
 * Factory definition for register controller and functions.
 * @name
 * @param {Object} $q
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "registerFactory",
  function registerFactoryFunction ($q) {
    return {

      /**
       * Verify if the user has access to the platform
       * @function isUserRegistered
       * @member integrates.registerFactory
       * @return {Object} Request result
       */
      "isUserRegistered" () {
        const oopsAc = "An error ocurred resolving user authorization";
        return $xhr.get($q, `${BASE.url}is_registered`, {
          "_": parseInt(
            secureRandom(5).join(""),
            10
          )
        }, oopsAc);
      },

      /**
       * Update legal notice acceptance status
       * @function updateLegalAcceptance
       * @member integrates.registerFactory
       * @param {String} status Value that indicates if the user has accepted
       * @return {Object} Request result
       */
      "updateLegalStatus" (status) {
        const oopsAc = "An error ocurred updating legal acceptance status";
        return $xhr.post($q, `${BASE.url}legal_status`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          status
        }, oopsAc);
      }
    };
  }
);
