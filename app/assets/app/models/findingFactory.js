/*eslint no-magic-numbers: ["error", { "ignore": [500, 401] }]*/
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
integrates.factory('findingFactory', function($q, $translate)
{
  return {

    /**
     * Invoca el servicio para tener los hallazgos de un proyecto
     * @function getVulnByName
     * @param {String} project
     * @member integrates.findingFactory
     * @return {Object}
     */
    getVulnByName: function(project, filter)
    {
      var oops_ac = $translate.instant('proj_alerts.error_text');
      return $xhr.get($q, BASE.url + "get_findings", {
        project: project, filter: filter, _: Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para tener los hallazgos de un proyecto por id
     * @function getVulnById
     * @param {String} id
     * @member integrates.findingFactory
     * @return {Object}
     */
    getVulnById: function(id)
    {
      var deferred = $q.defer();
      try 
      {
        $.ajax({
          url: BASE.url + "get_finding",
          method: "POST",
          data: {
            id: id,
            _: Math.random()
          },
          success: function (response) 
          {
            $(".loader").hide();
            deferred.resolve(response);
          },
          error: function (xhr, status) 
          {
            $(".loader").hide();
            if (xhr.status == 500)
            {
              Rollbar.error("Error: An error ocurred loading data");
              deferred.resolve({
                error: null,
                message: "Error interno cargando datos"
              });
            }
            else if (xhr.status == 401)
            {
              Rollbar.error("Error: 401 Unauthorized");
              location = "error401";
            }
          }
        });
      }
      catch (e) 
      {
        if (e.status == 401)
        {
          Rollbar.error("Error: 401 Unauthorized");
          location = "error401";
        }
        Rollbar.error("Error: An error ocurred getting finding by ID", e);
        deferred.resolve('exception');
      }
      return deferred.promise
    },

    /**
     * Invoca el servicio para tener el id de un proyecto
     * @function getIdByProject
     * @param {String} project
     * @member integrates.findingFactory
     * @return {Object}
     */
    getIdByProject: function(project)
    {
      var deferred = $q.defer();
      try 
      {
        $.ajax({
          url: BASE.url + "get_order",
          method: "GET",
          data: {
            project: project,
            _: Math.random()
          },
          success: function (response) 
          {
            $(".loader").hide();
            deferred.resolve(response);
          },
          error: function (xhr, status) 
          {
            $(".loader").hide();
            if (xhr.status == 500)
            {
              Rollbar.error("Error: An error ocurred loading data");
              deferred.resolve({
                error: null,
                message: "Error interno cargando datos"
              });
            }
            else if (xhr.status == 401)
            {
              Rollbar.error("Error: 401 Unauthorized");
              location = "error401";
            }
          }
        });
      }
      catch (e) 
      {
        if (e.status == 401)
        {
          Rollbar.error("Error: 401 Unauthorized");
          location = "error401";
        }
        Rollbar.error("Error: An error ocurred getting ID by project", e);
        deferred.resolve('exception');
      }
      return deferred.promise
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
    generateDoc: function(project, json, format)
    {
      var deferred = $q.defer();
      try 
      {
        $.ajax({
          url: BASE.url + "generate_autodoc?_"+Math.random(),
          method: "POST",
          data: {
            project: project,
            data: json,
            format: format
          },
          success: function (response) 
          {
            $(".loader").hide();
            deferred.resolve(response);
          },
          error: function (xhr, status) 
          {
            $(".loader").hide();
            if (xhr.status == 500)
            {
              Rollbar.error("Error: An error ocurred loading data");
              deferred.resolve({
                error: null,
                message: "Error interno cargando datos"
              });
            }
            else if (xhr.status == 401)
            {
              Rollbar.error("Error: 401 Unauthorized");
              location = "error401";
            }
          }
        });
      }
      catch (e) 
      {
        Rollbar.error("Error: An error ocurred generating document", e);
        deferred.resolve('exception');
      }
      return deferred.promise
    },

    /**
     * Invoca el servicio para actualizar un hallazgo
     * @function updateVuln
     * @param {String} project
     * @param {Object} json
     * @member integrates.findingFactory
     * @return {Object}
     */
    updateVuln: function(vuln)
    {
      var deferred = $q.defer();
      try 
      {
        $.ajax({
          url: BASE.url + "update_finding",
          method: "POST",
          data: {
            vuln: vuln
          },
          success: function (response) 
          {
            deferred.resolve(response);
          },
          error: function (xhr, status) 
          {
            $(".loader").hide();
            if (xhr.status == 500)
            {
              Rollbar.error("Error: An error ocurred loading data");
              deferred.resolve({
                error: null,
                message: "Error interno cargando datos"
              });
            }
            else if (xhr.status == 401)
            {
              Rollbar.error("Error: 401 Unauthorized");
              location = "error401";
            }
          }
        });
      }
      catch (e) 
      {
        if (e.status == 401)
        {
          Rollbar.error("Error: 401 Unauthorized");
          location = "error401";
        }
        Rollbar.error("Error: An error ocurred updating finding", e);
        deferred.resolve('exception');
      }
      return deferred.promise
    },

    /**
     * Invoca el servicio para eliminar un hallazgo
     * @function deleteVuln
     * @param {Object} vuln
     * @member integrates.findingFactory
     * @return {Object}
     */
    deleteVuln: function(vuln)
    {
      var deferred = $q.defer();
      try 
      {
        $.ajax({
          url: BASE.url + "delete_finding",
          method: "POST",
          data: {
            vuln: vuln
          },
          success: function (response) 
          {
            deferred.resolve(response);
          },
          error: function (xhr, status) 
          {
            $(".loader").hide();
            if (xhr.status == 500)
            {
              Rollbar.error("Error: An error ocurred loading data");
              deferred.resolve({
                error: null,
                message: "Error interno cargando datos"
              });
            }
            else if (xhr.status == 401)
            {
              Rollbar.error("Error: 401 Unauthorized");
              location = "error401";
            }
          }
        });
      }
      catch (e) 
      {
        if (e.status == 401)
        {
          Rollbar.error("Error: 401 Unauthorized");
          location = "error401";
        }
        Rollbar.error("Error: An error ocurred deleting finding", e);
        deferred.resolve('exception');
      }
      return deferred.promise
    },

    /**
     * Actualiza un pedido con su respectivo proyecto
     * @function updateOrderID
     * @param {Integer} id
     * @param {String} project
     * @member integrates.findingFactory
     * @return {Object}
     */
    updateOrderID: function(id, project)
    {
      var deferred = $q.defer();
      try 
      {
        $.ajax({
          url: BASE.url + "update_order",
          method: "POST",
          data: {
            project: project,
            id: id
          },
          success: function (response) 
          {
            deferred.resolve(response);
          },
          error: function (xhr, status) 
          {
            $(".loader").hide();
            if (xhr.status == 500)
            {
              deferred.resolve({
                error: null,
                message: "Error interno cargando datos"
              });
            }
            else if (xhr.status == 401)
            {
              location = "error401";
            }
          }
        });
      }
      catch (e) 
      {
        if (e.status == 401)
        {
          location = "error401";
        }
        else if (e.status == 500)
        {
          deferred.resolve({
            error: "undefined",
            message: "Error interno cargando datos"
          });
        }
        else 
        {
          deferred.resolve({
            error: "undefined",
            message: "Error desconocido"
          });
        }
      }
      return deferred.promise
    }
  }
});
