/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1,5]}]*/
/* global integrates, BASE, $xhr, $window,
$, Rollbar, eventsData, secureRandom, angular */
/**
 * @file projectFtry2.js
 * @author engineering@fluidattacks.com
 */
/**
 * Factory definition for some main set of functions.
 * @name projectFtry2
 * @param {Object} $q Angular constructor
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "projectFtry2",
  function projectFtry2 ($q) {
    return {

      /**
       * Give access to an user in a project
       * @function removeAccessIntegrates
       * @param {String} email Email of user to which access will be removed.
       * @param {String} project Project name.
       * @member integrates.projectFtry
       * @return {Object} Response of request
       */
      "removeAccessIntegrates" (email, project) {
        const oopsAc = "An error occurred getting events";
        return $xhr.post($q, `${BASE.url}remove_access_integrates`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          email,
          project
        }, oopsAc);
      },

      /**
       * Set the customer admin  of a project.
       * @function setProjectAdmin
       * @param {String} email Email of the new admin.
       * @member integrates.projectFtry2
       * @return {Object} Formstack response with the eventualities of a project
       */
      "setProjectAdmin" (email) {
        const oopsAc = "An error occurred getting events";
        return $xhr.post($q, `${BASE.url}set_project_admin`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          email
        }, oopsAc);
      }
    };
  }
);
