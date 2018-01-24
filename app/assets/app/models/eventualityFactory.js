/**
 * @file eventualityFactory.js
 * @author engineering@fluid.la
 */
/**
 * Crea el factory de la funcionalidad de eventualidades
 * @name
 * @param {Object} $q
 * @return {undefined}
 */
integrates.factory('eventualityFactory', function($q){
    return {
        /**
         * Obtiene los submission de una eventualidad
         * @function getEvntByName
         * @param {String} project
         * @member integrates.eventualityFactory
         * @return {Object}
         */
        getEvntByName: function(project, category){
          var deferred = $q.defer();
          try {
              $.ajax({
                  url: BASE.url + "get_eventualities",
                  data: {
                    project: project,
                    category: category
                  },
                  success: function (response) {
                      $(".loader").hide();
                      deferred.resolve(response);
                  },
                  error: function (xhr, status) {
                      $(".loader").hide();
                      if(xhr.status == 500){
                        Rollbar.error("Error: An error ocurred loading data");
                        deferred.resolve({
                            error: null,
                            message: "Error interno cargando datos"
                        });
                      }else if(xhr.status == 401){
                         Rollbar.error("Error: 401 Unauthorized");
                         location = "error401";
                      }
                  }
              });
          } catch (e) {
              if(e.status == 401){
                  Rollbar.error("Error: 401 Unauthorized");
                  location = "error401";
              }
              Rollbar.error("Error: An error ocurred getting event by name", e);
              deferred.resolve('exception');
          }
          return deferred.promise
        },
        /**
         * Actualiza una eventualidad
         * @function updateEvnt
         * @param {Object} vuln
         * @member integrates.eventualityFactory
         * @return {Object}
         */
        updateEvnt: function(vuln){
            var deferred = $q.defer();
            try {
                $.ajax({
                url: BASE.url + "update_eventuality",
                method: "POST",
                data: {
                    vuln: vuln
                  },
                  success: function (response) {
                      deferred.resolve(response);
                  },
                  error: function (xhr, status) {
                      $(".loader").hide();
                      if(xhr.status == 500){
                        Rollbar.error("Error: An error ocurred loading data");
                        deferred.resolve({
                            error: null,
                            message: "Error interno cargando datos"
                        });
                      }else if(xhr.status == 401){
                         Rollbar.error("Error: 401 Unauthorized");
                         location = "error401";
                      }
                  }
              });
          } catch (e) {
              if(e.status == 401){
                  Rollbar.error("Error: 401 Unauthorized");
                  location = "error401";
              }else if(e.status == 500){
                  Rollbar.error("Error: An error ocurred loading data");
                  deferred.resolve({
                    error: undefined,
                    message: "Error interno cargando datos"
                  });
              }else{
                  Rollbar.error("Error: An error ocurred updating event", e);
                  deferred.resolve({
                    error: undefined,
                    message: "Error desconocido"
                  });
              }
          }
          return deferred.promise
        }
    }
});
