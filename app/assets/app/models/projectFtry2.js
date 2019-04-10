/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1,5]}]*/
/* global integrates, BASE, $xhr, $window,
$, Rollbar, eventsData, secureRandom, angular, ldclient */
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
  function projectFtry2Function ($q) {
    return {

      /**
       * Validate that a user has access to a project.
       * @function accessToProject
       * @param {String} project Project name.
       * @member integrates.projectFtry2
       * @return {Object} Formstack response with the releases of a project
       */
      "accessToProject" (project) {
        const oopsAc = "An error occurred getting releases";
        return $xhr.get($q, `${BASE.url}access_to_project`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          project
        }, oopsAc);
      },

      /**
       * Get project information.
       * @function getProject
       * @param {String} projectName Project Name
       * @member integrates.projectFtry2
       * @return {Object} GraphQL response with the requested data
       */
      "getProject" (projectName) {
        const oopsAc = "An error occurred getting project information";
        const gQry = `{
          project (projectName: "${projectName}") {
            name
            openVulnerabilities
            subscription
          }
        }`;
        return $xhr.fetch($q, gQry, oopsAc);
      },

      /**
       * Get role of a user.
       * @function isCustomerAdmin
       * @param {String} project Project name.
       * @param {String} email User email.
       * @member integrates.projectFtry2
       * @return {Object} Formstack response with the releases of a project
       */
      "isCustomerAdmin" (project, email) {
        const oopsAc = "An error occurred getting user role";
        return $xhr.get($q, `${BASE.url}is_customer_admin`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          email,
          project
        }, oopsAc);
      }
    };
  }
);
