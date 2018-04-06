/* eslint no-magic-numbers: ["error", { "ignore": [500, 401] }]*/
/* global integrates, BASE, $xhr, $, Rollbar, window.location:true */
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
integrates.factory("eventualityFactory", function ($q) {
  return {

    /**
     * Obtiene los submission de una eventualidad
     * @function getEvntByName
     * @param {String} project
     * @member integrates.eventualityFactory
     * @return {Object}
     */
    "getEvntByName" (project, category) {
      const deferred = $q.defer();
      try {
        $.ajax({
          "data": {
            category,
            project
          },
          "error" (xhr, status) {
            $(".loader").hide();
            if (xhr.status == 500) {
              Rollbar.error("Error: An error ocurred loading data");
              deferred.resolve({
                "error": null,
                "message": "Error interno cargando datos"
              });
            }
            else if (xhr.status == 401) {
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
        if (err.status == 401) {
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
     * @param {Object} vuln
     * @member integrates.eventualityFactory
     * @return {Object}
     */
    "updateEvnt" (vuln) {
      const deferred = $q.defer();
      try {
        $.ajax({
          "data": {vuln},
          "error" (xhr, status) {
            $(".loader").hide();
            if (xhr.status == 500) {
              Rollbar.error("Error: An error ocurred loading data");
              deferred.resolve({
                "error": null,
                "message": "Error interno cargando datos"
              });
            }
            else if (xhr.status == 401) {
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
        if (err.status == 401) {
          Rollbar.error("Error: 401 Unauthorized");
          window.location = "error401";
        }
        else if (err.status == 500) {
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
  };
});
