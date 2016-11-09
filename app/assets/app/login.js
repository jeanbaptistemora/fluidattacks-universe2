/*
 * @description: Controlador y servicio para autenticacion en FLUIDIntegrates
 */

var BASE = { production: "/integrates/",
             development: "/" };
BASE.url = BASE.development;
//definicion de modulos
var integrates = angular.module("FluidIntegrates", []); 

integrates.controller("loginController", function($scope){

    $scope.login = function(){
        var username = $scope.username;
        var password = $scope.password;
        if(typeof(username) != "string" 
            || typeof(password) != "string"){
             $.gritter.add({
                title: '',
                text: "Usuario/Clave son obligatorios",
                class_name: 'color warning',
                sticky: false,
            }); 
        }else if(username.trim() == "" 
            || password.trim() == ""){
            $.gritter.add({
                title: '',
                text: "Usuario/Clave son obligatorios",
                class_name: 'color warning',
                sticky: false,
            });
        }else{
            $.ajax({
                url: "login/",
                method: "POST",
                data: {
                    user: username,
                    pass: password
                }
            }).done(function(e){
                var color = (e.error == true)?"warning":"success";
                $.gritter.add({
                    title: '',
                    text: e.message,
                    class_name: 'color '+color,
                    sticky: false,
                }); 
                if(color == "success"){
                    setTimeout("location = '/dashboard';",2000);
                }
            })
        }
    };

});