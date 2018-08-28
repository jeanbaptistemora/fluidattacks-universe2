/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1, 5] }]*/
/* global integrates, BASE, $xhr, $, Rollbar, angular, secureRandom */
/**
 * @file dashboardFtry.js
 * @author engineering@fluidattacks.com
 */
/**
 * Factory definition for dashboard controler and functions.
 * @name
 * @param {Object} $q
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "dashboardFtry",
  function dashboardFtry ($q) {
    return {
      "getMyProjects" () {
        const oopsAc = "An error ocurred getting projects list";
        return $xhr.get(
          $q, `${BASE.url}get_myprojects`,
          {"_": parseInt(secureRandom(5).join(""), 10)}, oopsAc
        );
      }
    };
  }
);
