integrates.factory('searchFactory', function($q){
    return {
        getVulnByName: function(project){
          var deferred = $q.defer();
          try {
              $.ajax({
                  url: BASE.url + "get_vuln_by_name",
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
                            error: null, 
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
     	},
        getVulnByDate: function(from, to){
          var deferred = $q.defer();
          try {
              $.ajax({
                  url: BASE.url + "get_vuln_by_date",
                  data: {
                    from: from,
                    to: to
                  },
                  success: function (response) { 
                      deferred.resolve(response);
                  },
                  error: function (xhr, status) {
                      self.ajaxError(xhr, status);
                      deferred.resolve('error');
                  }
              });
          } catch (e) {
              console.log('There was an exception: ' + e.message);
              deferred.resolve('exception');
          }
          return deferred.promise
        },
        getEvntByName: function(project){
          var deferred = $q.defer();
          try {
              $.ajax({
                  url: BASE.url + "get_evnt_by_name",
                  data: {
                    project: project
                  },
                  success: function (response) { 
                      deferred.resolve(response);
                  },
                  error: function (xhr, status) {
                      self.ajaxError(xhr, status);
                      deferred.resolve('error');
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