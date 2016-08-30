integrates.controller("loginController", function($scope, loginFactory) {
    $scope.login = function(){
        var username = $scope.username;
        var password = $scope.password;
        if(typeof username == "string" 
            && typeof password == "string"){
            if(username.trim() != ""
                 || password.trim() != ""){
                    loginFactory.login(username,password);
                    $.gritter.add({
                        title: 'Login Success',
                        text: 'You will be redirected',
                        class_name: 'color success',
                        sticky: false,
                    });
                    return false;
                 }
        }
        $.gritter.add({
            title: 'Login Fail',
            text: 'Username and password are mandatory',
            class_name: 'color warning',
            sticky: false,
        });
    }
});