integrates.factory('findingFactory', function($q){
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
        generateDoc: function(project,json){
          var deferred = $q.defer();
          try {
              $.ajax({
                  url: BASE.url + "generate_auto_doc",
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
                      console.log(xhr);
                      if(xhr.status == 500){
                        deferred.resolve({
                            error: null, 
                            message: "Service error"
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
                      deferred.resolve('error');
                  }
              });
          } catch (e) {
              console.log('There was an exception: ' + e.message);
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