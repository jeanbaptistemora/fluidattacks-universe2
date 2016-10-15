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
                      console.log(xhr);
                      if(xhr.status == 500){
                        deferred.resolve({
                            error: true, 
                            message: "Formstack error"
                        });
                      }     
                  }
              });
          } catch (e) {
              console.log('There was an exception: ' + e.message);
              deferred.resolve('exception');
          }
          return deferred.promise
        }
    }
});