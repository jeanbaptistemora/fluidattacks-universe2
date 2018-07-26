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
       * Update legal notice acceptance status
       * @function acceptLegal
       * @member integrates.registerFactory
       * @param {boolean} remember remember acceptance decision
       * @return {Object} Request result
       */
      "acceptLegal" (remember) {
        const oopsAc = "An error ocurred updating legal acceptance status";
        return $xhr.post($q, `${BASE.url}accept_legal`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          remember
        }, oopsAc);
      },

      /**
       * Get authorization and remember preferences info
       * @function getLoginInfo
       * @member integrates.registerFactory
       * @return {Object} Request result
       */
      "getLoginInfo" () {
        const oopsAc = "An error ocurred resolving user authorization";
        return $xhr.get($q, `${BASE.url}get_login_info`, {
          "_": parseInt(
            secureRandom(5).join(""),
            10
          )
        }, oopsAc);
      }
    };
  }
);
