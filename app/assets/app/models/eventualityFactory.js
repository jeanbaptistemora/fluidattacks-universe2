/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global integrates, BASE, $xhr, $, Rollbar, angular, $window */
/**
 * @file eventualityFactory.js
 * @author engineering@fluidattacks.com
 */
/**
 * Factory definition for eventuality controler and functions.
 * @name
 * @param {Object} $q
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "eventualityFactory",
  function eventualityFactory (
    $q,
    $window
  ) {
    return {

      /**
       * Return the eventualities of a project
       * @function getEvntByName
       * @param {String} project Project Name
       * @param {String} category Search filter: By Name or ID
       * @member integrates.eventualityFactory
       * @return {Object} Formstack response with the eventualities of a project
       */
      "getEvntByName" (project, category) {
        const INTERNAL_SERVER_ERROR = 500;
        const UNAUTHORIZED_ERROR = 401;
        try {
          $.ajax({
            "data": {
              category,
              project
            },
            "error" (xhr) {
              angular.element(".loader").hide();
              if (xhr.status === INTERNAL_SERVER_ERROR) {
                Rollbar.error("Error: An error ocurred loading data");
                return $q.when({
                  "error": null,
                  "message": "Error interno cargando datos"
                });
              }
              else if (xhr.status === UNAUTHORIZED_ERROR) {
                Rollbar.error("Error: 401 Unauthorized");
                $window.location = "error401";
                return false;
              }
              return true;
            },
            "success" (response) {
              angular.element(".loader").hide();
              return $q.when(response);
            },
            "url": `${BASE.url}get_eventualities`
          });
        }
        catch (err) {
          if (err.status === UNAUTHORIZED_ERROR) {
            Rollbar.error("Error: 401 Unauthorized");
            $window.location = "error401";
          }
          Rollbar.error("Error: An error ocurred getting event by name", err);
          return $q.when("exception");
        }
        return true;
      },

      /**
       * Update an eventuality
       * @function updateEvnt
       * @param {Object} vuln New data about an eventuality
       * @member integrates.eventualityFactory
       * @return {Object} Formstack response about update request
       */
      "updateEvnt" (vuln) {
        const INTERNAL_SERVER_ERROR = 500;
        const UNAUTHORIZED_ERROR = 401;
        try {
          $.ajax({
            "data": {vuln},
            "error" (xhr) {
              angular.element(".loader").hide();
              if (xhr.status === INTERNAL_SERVER_ERROR) {
                Rollbar.error("Error: An error ocurred loading data");
                return $q.when({
                  "error": null,
                  "message": "Error interno cargando datos"
                });
              }
              else if (xhr.status === UNAUTHORIZED_ERROR) {
                Rollbar.error("Error: 401 Unauthorized");
                $window.location = "error401";
              }
              return true;
            },
            "method": "POST",
            "success" (response) {
              return $q.when(response);
            },
            "url": `${BASE.url}update_eventuality`
          });
        }
        catch (err) {
          if (err.status === UNAUTHORIZED_ERROR) {
            Rollbar.error("Error: 401 Unauthorized");
            $window.location = "error401";
          }
          else if (err.status === INTERNAL_SERVER_ERROR) {
            Rollbar.error("Error: An error ocurred loading data");
            return $q.when({
              "error": "undefined",
              "message": "Error interno cargando datos"
            });
          }
          else {
            Rollbar.error("Error: An error ocurred updating event", err);
            return $q.when({
              "error": "undefined",
              "message": "Error desconocido"
            });
          }
        }
        return true;
      }
    };
  }
);
