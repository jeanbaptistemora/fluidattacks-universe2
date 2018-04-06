/* eslint no-magic-numbers: ["error", { "ignore": [500, 401] }]*/
/* global integrates, BASE, $xhr, $, Rollbar, window.location:true */
/**
 * @file findingFactory.js
 * @author engineering@fluidattacks.com
 */
/**
 * Crea el factory de la funcionalidad de hallazgos
 * @name findingFactory
 * @param {Object} $q
 * @return {undefined}
 */
/** @export */
integrates.factory("findingFactory", function ($q, $translate) {
  return {

    /**
     * Invoca el servicio para eliminar un hallazgo
     * @function deleteVuln
     * @param {Object} vuln
     * @member integrates.findingFactory
     * @return {Object}
     */
    "deleteVuln" (vuln) {
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
          "url": `${BASE.url}delete_finding`

        });
      }
      catch (err) {
        if (err.status == 401) {
          Rollbar.error("Error: 401 Unauthorized");
          window.location = "error401";
        }
        Rollbar.error("Error: An error ocurred deleting finding", err);
        deferred.resolve("exception");
      }
      return deferred.promise;
    },

    /**
     * Invoca el servicio para crear el proceso que genera
     * la documentacion de un proyecto
     * @function generateDoc
     * @param {String} project
     * @param {Object} json
     * @member integrates.findingFactory
     * @return {Object}
     */
    "generateDoc" (project, json, format) {
      const deferred = $q.defer();
      try {
        $.ajax({
          "data": {
            "data": json,
            format,
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
          "method": "POST",
          "success" (response) {
            $(".loader").hide();
            deferred.resolve(response);
          },
          "url": `${BASE.url}generate_autodoc?_${Math.random()}`
        });
      }
      catch (err) {
        Rollbar.error("Error: An error ocurred generating document", err);
        deferred.resolve("exception");
      }
      return deferred.promise;
    },

    /**
     * Invoca el servicio para tener el id de un proyecto
     * @function getIdByProject
     * @param {String} project
     * @member integrates.findingFactory
     * @return {Object}
     */
    "getIdByProject" (project) {
      const deferred = $q.defer();
      try {
        $.ajax({
          "data": {
            "_": Math.random(),
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
          "method": "GET",
          "success" (response) {
            $(".loader").hide();
            deferred.resolve(response);
          },
          "url": `${BASE.url}get_order`
        });
      }
      catch (err) {
        if (err.status == 401) {
          Rollbar.error("Error: 401 Unauthorized");
          window.location = "error401";
        }
        Rollbar.error("Error: An error ocurred getting ID by project", err);
        deferred.resolve("exception");
      }
      return deferred.promise;
    },

    /**
     * Invoca el servicio para tener los hallazgos de un proyecto por id
     * @function getVulnById
     * @param {String} id
     * @member integrates.findingFactory
     * @return {Object}
     */
    "getVulnById" (id) {
      const deferred = $q.defer();
      try {
        $.ajax({
          "data": {
            "_": Math.random(),
            id
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
          "method": "POST",
          "success" (response) {
            $(".loader").hide();
            deferred.resolve(response);
          },
          "url": `${BASE.url}get_finding`
        });
      }
      catch (err) {
        if (err.status == 401) {
          Rollbar.error("Error: 401 Unauthorized");
          window.location = "error401";
        }
        Rollbar.error("Error: An error ocurred getting finding by ID", err);
        deferred.resolve("exception");
      }
      return deferred.promise;
    },

    /**
     * Invoca el servicio para tener los hallazgos de un proyecto
     * @function getVulnByName
     * @param {String} project
     * @member integrates.findingFactory
     * @return {Object}
     */
    "getVulnByName" (project, filter) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.get($q, `${BASE.url}get_findings`, {
        "_": Math.random(),
        filter,
        project
      }, oops_ac);
    },

    /**
     * Actualiza un pedido con su respectivo proyecto
     * @function updateOrderID
     * @param {Integer} id
     * @param {String} project
     * @member integrates.findingFactory
     * @return {Object}
     */
    "updateOrderID" (id, project) {
      const deferred = $q.defer();
      try {
        $.ajax({
          "data": {
            id,
            project
          },
          "error" (xhr, status) {
            $(".loader").hide();
            if (xhr.status == 500) {
              deferred.resolve({
                "error": null,
                "message": "Error interno cargando datos"
              });
            }
            else if (xhr.status == 401) {
              window.location = "error401";
            }
          },
          "method": "POST",
          "success" (response) {
            deferred.resolve(response);
          },
          "url": `${BASE.url}update_order`
        });
      }
      catch (err) {
        if (err.status == 401) {
          window.location = "error401";
        }
        else if (err.status == 500) {
          deferred.resolve({
            "error": "undefined",
            "message": "Error interno cargando datos"
          });
        }
        else {
          deferred.resolve({
            "error": "undefined",
            "message": "Error desconocido"
          });
        }
      }
      return deferred.promise;
    },

    /**
     * Invoca el servicio para actualizar un hallazgo
     * @function updateVuln
     * @param {String} project
     * @param {Object} json
     * @member integrates.findingFactory
     * @return {Object}
     */
    "updateVuln" (vuln) {
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
          "url": `${BASE.url}update_finding`
        });
      }
      catch (err) {
        if (err.status == 401) {
          Rollbar.error("Error: 401 Unauthorized");
          window.location = "error401";
        }
        Rollbar.error("Error: An error ocurred updating finding", err);
        deferred.resolve("exception");
      }
      return deferred.promise;
    }
  };
});
