/**
 * @file login.js
 */
/*
 *  Seleccion de rutas absolutas para el direccionamiento
 *  de integrates
 */
var BASE = { production: "/integrates/",
             development: "/" };
BASE.url = BASE.production;
if(location.pathname.indexOf("/integrates") == -1)
    BASE.url = BASE.development;
//definicion de modulos
var integrates = angular.module("FluidIntegrates", []); 
/**
 * Crea el controlador de la funcionalidad de autenticacion
 * @name loginController 
 * @param {Object} $scope 
 * @param {integrates.loginFactory} loginFactory 
 * @return {undefined}
 */
integrates.controller("loginController", function($scope){
    /**
     * Autentica a un usuario
     * @function login
     * @return {undefined}
     */
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
                    redirector = function(){
                        location = BASE.url + "dashboard";
                    }
                    setTimeout(redirector,2000);
                }
            })
        }
    };

});