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
    {BASE.url = BASE.development;}
//definicion de modulos
var integrates = angular.module("FluidIntegrates", ['ngSanitize','pascalprecht.translate']);

integrates.config(['$translateProvider', function($translateProvider) {
    var translations = {
        'login_message': 'Please log in to proceed.',
        'login_welcome': 'If you are a new user, you must call a FLUID representative to register.',
        'button': {
            'google': 'Log in with Google',
            'azure': 'Log in with Azure/Office365'
        }
    };
    var traducciones = {
        'login_message': 'Porfavor ingrese.',
        'login_welcome': 'Si eres un usuario nuevo, debes llamar a tu representante de FLUID para registrarte',
        'button': {
            'google': 'Ingresar con Google',
            'azure': 'Ingresar con Azure/Office365'
        }
    };
    $translateProvider.useSanitizeValueStrategy('sanitize');
    $translateProvider.
    translations('en', translations).
    translations('es', traducciones).
    preferredLanguage('en');
}]);
/*
 * MixPanel localhost Fixer
 */
integrates.isProduction = function(){
    return location.toString().indexOf("localhost:8000") == -1;
};
/**
 * Crea el controlador de la funcionalidad de autenticacion
 * @name loginController
 * @param {Object} $scope
 * @param {integrates.loginFactory} loginFactory
 * @return {undefined}
 */
integrates.controller("loginController", function($scope, $translate){
    /**
     * Autentica a un usuario
     * @function login
     * @return {undefined}
     */
    $scope.login = function(){
        var username = $scope.username;
        var password = $scope.password;
        if(typeof username != "string"
            || typeof password != "string"){
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
                url: BASE.url + "login/",
                method: "POST",
                data: {
                    user: username,
                    pass: password
                }
            }).done(function(e){
                var color = e.error == true?"warning":"success";
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

    $scope.lang = function (langKey) {
        if(langKey == "es"
			|| langKey == "en"){
			localStorage.lang = langKey;
		}
		$translate.use(localStorage.lang);
    };


});
