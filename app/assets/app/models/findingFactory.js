/**
 * @file findingFactory.js
 * @author engineering@fluid.la
 */
/**
 * Crea el factory de la funcionalidad de hallazgos
 * @name findingFactory 
 * @param {Object} $q 
 * @return {undefined}
 */
integrates.factory('findingFactory', function($q){
    return {
        /**
         * Invoca el servicio para tener los hallazgos de un proyecto
         * @function getVulnByName
         * @param {String} project
         * @member integrates.findingFactory
         * @return {Object}
         */
        getVulnByName: function(project, filter){
          var deferred = $q.defer();
          try {
              $.ajax({
                  url: BASE.url + "get_vuln_by_name",
                  data: {
                    project: project,
                    filter: filter,
                    _: Math.random()
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
         * Invoca el servicio para tener los hallazgos de un proyecto por id
         * @function getVulnById
         * @param {String} id
         * @member integrates.findingFactory
         * @return {Object}
         */
        getVulnById: function(id){
          var deferred = $q.defer();
          try {
              $.ajax({
                  url: BASE.url + "get_vuln_by_id",
                  method: "POST",
                  data: {
                    id: id,
                    _: Math.random()
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
         * Invoca el servicio para tener el id de un proyecto
         * @function getIdByProject
         * @param {String} project
         * @member integrates.findingFactory
         * @return {Object}
         */
        getIdByProject: function(project){
          var deferred = $q.defer();
          try {
              $.ajax({
                  url: BASE.url + "get_order",
                  method: "GET",
                  data: {
                    project: project,
                    _: Math.random()
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
         * Invoca el servicio para crear el proceso que genera 
         * la documentacion de un proyecto
         * @function generateDoc
         * @param {String} project
         * @param {Object} json
         * @member integrates.findingFactory
         * @return {Object}
         */
        generateDoc: function(project, json, format){
          var deferred = $q.defer();
          try {
              $.ajax({
                  url: BASE.url + "generate_autodoc?_"+Math.random(),
                  method: "POST",
                  data: {
                    project: project,
                    data: json,
                    format: format
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
              console.log('There was an exception: ' + e.message);
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
        updateVuln: function(vuln){
            var deferred = $q.defer();
            try {
                $.ajax({
                url: BASE.url + "update_vuln",
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
              }
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
        deleteVuln: function(vuln){
            var deferred = $q.defer();
            try {
                $.ajax({
                url: BASE.url + "delete_vuln",
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
              }
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
        updateOrderID: function(id, project){
            var deferred = $q.defer();
            try {
                $.ajax({
                    url: BASE.url + "update_order_id",
                    method: "POST",
                    data: {
                        project: project,
                        id: id
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