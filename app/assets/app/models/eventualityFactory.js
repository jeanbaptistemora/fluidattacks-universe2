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
                  url: BASE.url + "get_evnt_by_name",
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
                        deferred.resolve({
                            error: null, 
                            message: "Error de formstack"
                        });
                      }else if(xhr.status == 401){
                         location = "/index"; 
                      }    
                  }
              });
          } catch (e) {
              if(e.status == 401){
                  location = "/index";
              }
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
                url: BASE.url + "update_evnt",
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
                        deferred.resolve({
                            error: null, 
                            message: "Error de formstack"
                        });
                      }else if(xhr.status == 401){
                         location = "/index"; 
                      }    
                  }
              });
          } catch (e) {
              if(e.status == 401){
                  location = "/index";
              }else if(e.status == 500){
                  deferred.resolve({
                    error: undefined, 
                    message: "Error de formstack"
                  });
              }else{
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