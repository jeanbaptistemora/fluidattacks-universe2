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
        let gQry = `mutation {
          acceptLegal(remember:$rem){
            success
          }
        }`;
        gQry = gQry.replace("$rem", remember);
        return $xhr.fetch($q, gQry, oopsAc);
      },

      /**
       * Get authorization and remember preferences
       * @function getLoginInfo
       * @member integrates.registerFactory
       * @return {Object} Request result
       */
      "getLoginInfo" () {
        const oopsAc = "An error ocurred resolving user authorization";
        const gQry = `{
          login{
            authorized
            remember
          }
        }`;
        return $xhr.fetch($q, gQry, oopsAc);
      }
    };
  }
);
