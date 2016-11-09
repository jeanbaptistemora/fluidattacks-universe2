integrates.factory('findingFactory', function($q){
    return {
        getVulnByName: function(project){
          var deferred = $q.defer();
          try {
              $.ajax({
                  url: BASE.url + "get_vuln_by_name",
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
        generateDoc: function(project,json){
          var deferred = $q.defer();
          try {
              console.log(json);
              $.ajax({
                  url: BASE.url + "generate_autodoc?_"+Math.random(),
                  method: "POST",
                  data: {
                    project: project,
                    data: json
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
        }
    }
});