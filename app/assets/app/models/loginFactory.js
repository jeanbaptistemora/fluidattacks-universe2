integrates.factory('loginFactory', function($q){
    return {
        login : function(username, password){
          var deferred = $q.defer();
          try {
              $.ajax({
                  url: BASE.url + "login",
                  type: 'POST',
                  data: {
                    username: username,
                    password: password
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