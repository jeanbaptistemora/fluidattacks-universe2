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
       * Admin accept a release.
       * @function acceptRelease
       * @param {String} id Finding id.
       * @member integrates.projectFtry2
       * @return {Object} Formstack response with updated data
       */
      "acceptRelease" (id) {
        const oopsAc = "An error occurred accepting release";
        return $xhr.post($q, `${BASE.url}accept_release`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          id
        }, oopsAc);
      },

      /**
       * Admin reject a release.
       * @function rejectRelease
       * @param {String} data Reject data.
       * @member integrates.projectFtry2
       * @return {Object} Formstack response with updated data
       */
      "rejectRelease" (data) {
        const oopsAc = "An error occurred rejecting release";
        return $xhr.post($q, `${BASE.url}reject_release`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data
        }, oopsAc);
      },

      /**
       * Get releases by project name.
       * @function releasesByName
       * @param {String} project Project name.
       * @member integrates.projectFtry2
       * @return {Object} Formstack response with the releases of a project
       */
      "releasesByName" (project) {
        const oopsAc = "An error occurred getting releases";
        return $xhr.get($q, `${BASE.url}get_releases`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          project
        }, oopsAc);
      },

      /**
       * Give access to an user in a project
       * @function removeAccessIntegrates
       * @param {String} email Email of user to which access will be removed.
       * @param {String} project Project name.
       * @member integrates.projectFtry
       * @return {Object} Response of request
       */
      "removeAccessIntegrates" (email, project) {
        const oopsAc = "An error occurred removing access to an user";
        return $xhr.post($q, `${BASE.url}remove_access_integrates`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          email,
          project
        }, oopsAc);
      },

      /**
       * Remove a customer admin  of a project.
       * @function removeProjectAdmin
       * @param {String} email Email of the new admin.
       * @member integrates.projectFtry2
       * @return {Object} Response by SQL DB
       */
      "removeProjectAdmin" (email) {
        const oopsAc = "An error occurred setting project admin";
        return $xhr.post($q, `${BASE.url}remove_project_admin`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          email
        }, oopsAc);
      },

      /**
       * Set the customer admin  of a project.
       * @function setProjectAdmin
       * @param {String} email Email of the new admin.
       * @member integrates.projectFtry2
       * @return {Object} Response by SQL DB
       */
      "setProjectAdmin" (email) {
        const oopsAc = "An error occurred setting project admin";
        return $xhr.post($q, `${BASE.url}set_project_admin`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          email
        }, oopsAc);
      }
    };
  }
);
