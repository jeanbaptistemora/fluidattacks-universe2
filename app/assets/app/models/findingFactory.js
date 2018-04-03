/* eslint no-magic-numbers: ["error", { "ignore": [500, 401] }]*/
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
integrates.factory("findingFactory", function ($q, $translate) {
  return {

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
        project,
        filter,
        "_": Math.random()
      }, oops_ac);
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
          "url": `${BASE.url}get_finding`,
          "method": "POST",
          "data": {
            id,
            "_": Math.random()
          },
          "success" (response) {
            $(".loader").hide();
            deferred.resolve(response);
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
              location = "error401";
            }
          }
        });
      }
      catch (e) {
        if (e.status == 401) {
          Rollbar.error("Error: 401 Unauthorized");
          location = "error401";
        }
        Rollbar.error("Error: An error ocurred getting finding by ID", e);
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
          "url": `${BASE.url}get_order`,
          "method": "GET",
          "data": {
            project,
            "_": Math.random()
          },
          "success" (response) {
            $(".loader").hide();
            deferred.resolve(response);
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
              location = "error401";
            }
          }
        });
      }
      catch (e) {
        if (e.status == 401) {
          Rollbar.error("Error: 401 Unauthorized");
          location = "error401";
        }
        Rollbar.error("Error: An error ocurred getting ID by project", e);
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
          "url": `${BASE.url}generate_autodoc?_${Math.random()}`,
          "method": "POST",
          "data": {
            project,
            "data": json,
            format
          },
          "success" (response) {
            $(".loader").hide();
            deferred.resolve(response);
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
              location = "error401";
            }
          }
        });
      }
      catch (e) {
        Rollbar.error("Error: An error ocurred generating document", e);
        deferred.resolve("exception");
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
          "url": `${BASE.url}update_finding`,
          "method": "POST",
          "data": {vuln},
          "success" (response) {
            deferred.resolve(response);
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
              location = "error401";
            }
          }
        });
      }
      catch (e) {
        if (e.status == 401) {
          Rollbar.error("Error: 401 Unauthorized");
          location = "error401";
        }
        Rollbar.error("Error: An error ocurred updating finding", e);
        deferred.resolve("exception");
      }
      return deferred.promise;
    },

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
          "url": `${BASE.url}delete_finding`,
          "method": "POST",
          "data": {vuln},
          "success" (response) {
            deferred.resolve(response);
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
              location = "error401";
            }
          }
        });
      }
      catch (e) {
        if (e.status == 401) {
          Rollbar.error("Error: 401 Unauthorized");
          location = "error401";
        }
        Rollbar.error("Error: An error ocurred deleting finding", e);
        deferred.resolve("exception");
      }
      return deferred.promise;
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
          "url": `${BASE.url}update_order`,
          "method": "POST",
          "data": {
            project,
            id
          },
          "success" (response) {
            deferred.resolve(response);
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
              location = "error401";
            }
          }
        });
      }
      catch (e) {
        if (e.status == 401) {
          location = "error401";
        }
        else if (e.status == 500) {
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
    }
  };
});
