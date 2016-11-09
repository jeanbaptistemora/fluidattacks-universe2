integrates.factory('eventualityFactory', function($q){
    return {
        getEvntByName: function(project){
          var deferred = $q.defer();
          try {
              $.ajax({
                  url: BASE.url + "get_evnt_by_name",
                  data: {
                    project: project
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
              }
              deferred.resolve('exception');
          }
          return deferred.promise
        }
    }
});