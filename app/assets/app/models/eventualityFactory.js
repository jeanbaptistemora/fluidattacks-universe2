/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global integrates, BASE, $xhr, $, Rollbar, window.location:true, angular */
/**
 * @file eventualityFactory.js
 * @author engineering@fluidattacks.com
 */
/**
 * Crea el factory de la funcionalidad de eventualidades
 * @name
 * @param {Object} $q
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory("eventualityFactory", ($q) => ({

  /**
   * Obtiene los submission de una eventualidad
   * @function getEvntByName
   * @param {String} project Project Name
   * @param {String} category Search filter: By Name or ID
   * @member integrates.eventualityFactory
   * @return {Object} Formstack response with the eventualities of a project
   */
  "getEvntByName" (project, category) {
    const INTERNAL_SERVER_ERROR = 500;
    const UNAUTHORIZED_ERROR = 401;
    const deferred = $q.defer();
    try {
      $.ajax({
        "data": {
          category,
          project
        },
        "error" (xhr) {
          $(".loader").hide();
          if (xhr.status === INTERNAL_SERVER_ERROR) {
            Rollbar.error("Error: An error ocurred loading data");
            deferred.resolve({
              "error": null,
              "message": "Error interno cargando datos"
            });
          }
          else if (xhr.status === UNAUTHORIZED_ERROR) {
            Rollbar.error("Error: 401 Unauthorized");
            window.location = "error401";
          }
        },
        "success" (response) {
          $(".loader").hide();
          deferred.resolve(response);
        },
        "url": `${BASE.url}get_eventualities`
      });
    }
    catch (err) {
      if (err.status === UNAUTHORIZED_ERROR) {
        Rollbar.error("Error: 401 Unauthorized");
        window.location = "error401";
      }
      Rollbar.error("Error: An error ocurred getting event by name", err);
      deferred.resolve("exception");
    }
    return deferred.promise;
  },

  /**
   * Actualiza una eventualidad
   * @function updateEvnt
   * @param {Object} vuln New data about an eventuality
   * @member integrates.eventualityFactory
   * @return {Object} Formstack response about update request
   */
  "updateEvnt" (vuln) {
    const INTERNAL_SERVER_ERROR = 500;
    const UNAUTHORIZED_ERROR = 401;
    const deferred = $q.defer();
    try {
      $.ajax({
        "data": {vuln},
        "error" (xhr) {
          $(".loader").hide();
          if (xhr.status === INTERNAL_SERVER_ERROR) {
            Rollbar.error("Error: An error ocurred loading data");
            deferred.resolve({
              "error": null,
              "message": "Error interno cargando datos"
            });
          }
          else if (xhr.status === UNAUTHORIZED_ERROR) {
            Rollbar.error("Error: 401 Unauthorized");
            window.location = "error401";
          }
        },
        "method": "POST",
        "success" (response) {
          deferred.resolve(response);
        },
        "url": `${BASE.url}update_eventuality`
      });
    }
    catch (err) {
      if (err.status === UNAUTHORIZED_ERROR) {
        Rollbar.error("Error: 401 Unauthorized");
        window.location = "error401";
      }
      else if (err.status === INTERNAL_SERVER_ERROR) {
        Rollbar.error("Error: An error ocurred loading data");
        deferred.resolve({
          "error": "undefined",
          "message": "Error interno cargando datos"
        });
      }
      else {
        Rollbar.error("Error: An error ocurred updating event", err);
        deferred.resolve({
          "error": "undefined",
          "message": "Error desconocido"
        });
      }
    }
    return deferred.promise;
  }
}));
