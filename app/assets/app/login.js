// This file should not be renamed
/* eslint-disable angular/file-name */
// Login page is isolated from the rest of the application.
/* eslint-disable angular/component-limit*/
/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global angular,$, $timeout,redirector:true, $window */
/**
 * @file login.js
 */
/*
 *  Seleccion de rutas absolutas para el direccionamiento
 *  de integrates
 */
const BASE = {
  "development": "/",
  "production": "/integrates/"
};
BASE.url = BASE.production;
// eslint-disable-next-line angular/window-service
if (window.location.pathname.indexOf("/integrates") === -1) {
  BASE.url = BASE.development;
}
// Definicion de modulos
angular.module("FluidIntegrates", [
  "ngSanitize",
  "pascalprecht.translate"
]);

angular.module("FluidIntegrates").config([
  "$translateProvider",

  /*
   * Angular module configuration only can
   *be made with parameter array injection
   */
  /* eslint-disable-next-line angular/di */
  function config ($translateProvider) {
    const translations = {
      "button": {
        "azure": "Log in with Azure/Office365",
        "google": "Log in with Google"
      },
      "login_message": "Please log in to proceed.",
      "login_recommend": "We strongly recommend you to use 2-Step " +
                          "verification. For more information please visit:",
      "login_welcome": "If you are a new user, you must call a " +
                       "FLUID representative to register."
    };
    const traducciones = {
      "button": {
        "azure": "Ingresar con Azure/Office365",
        "google": "Ingresar con Google"
      },
      "login_message": "Porfavor ingrese.",
      "login_recommend": "Te recomendamos encarecidamente el uso de un " +
                          "segundo factor de autenticación, para más " +
                          "información visita:",
      "login_welcome": "Si eres un usuario nuevo, debes llamar a tu " +
                       "representante de FLUID para registrarte."
    };
    $translateProvider.useSanitizeValueStrategy("sanitize");
    if (angular.isUndefined(localStorage.lang)) {
      localStorage.lang = "en";
    }
    $translateProvider.
      translations("en", translations).
      translations("es", traducciones).
      preferredLanguage(localStorage.lang);
  }
]);

/*
 * MixPanel localhost Fixer
 */
angular.module("FluidIntegrates").isProduction = function isProduction () {
  // eslint-disable-next-line angular/window-service
  return window.location.toString().indexOf("localhost:8000") === -1;
};

/**
 * Crea el controlador de la funcionalidad de autenticacion
 * @name loginCtrl
 * @param {Object} $scope
 * @param {integrates.loginFactory} loginFactory
 * @return {undefined}
 */
angular.module("FluidIntegrates").controller(
  "loginCtrl",
  function loginCtrl (
    $scope,
    $translate
  ) {
    $scope.lang = function lang (langKey) {
      if (langKey === "es" || langKey === "en") {
        localStorage.lang = langKey;
        location.reload();
      }
      $translate.use(localStorage.lang);
    };
    $.gritter.add({
      "class_name": "color info",
      "sticky": true,
      "text": `${$translate.instant("login_recommend")}<br><br> <div ` +
                  "class=\"text-center\"><a class=\"btn btn-danger google " +
                  "login-button\" href=\"http://bit.ly/2Gpjt6h\" " +
                  "onclick=\"mixPanelReport('Click Google 2 factor');\" " +
                  "target=\"_blank\"><i class=\"fa fa-google-plus fa-2x " +
                  "pull-left\" aria-hidden=\"true\"></i></a>" +
                  "<a class=\"btn btn-primary azure\" " +
                  "onclick=\"mixPanelReport('Click Azure 2 factor');\" " +
                  "href=\"http://bit.ly/2Gp1L2X\" target=\"_blank\"><img " +
                  "src=\"assets/img/azure.png\" class=\"fa fa-azure " +
                  "fa-2x pull-left\" aria-hidden=\"true\" height=\"25\">" +
                  "</img></a></div>",
      "title": ""
    });

    /**
     * Autentica a un usuario
     * @function login
     * @return {undefined}
     */
    $scope.login = function login () {
      const userName = $scope.username;
      const pass = $scope.password;
      if (typeof userName != "string" ||
            typeof pass != "string") {
        $.gritter.add({
          "class_name": "color warning",
          "sticky": false,
          "text": "Usuario/Clave son obligatorios",
          "title": ""
        });
      }
      else if (userName.trim() === "" ||
            pass.trim() === "") {
        $.gritter.add({
          "class_name": "color warning",
          "sticky": false,
          "text": "Usuario/Clave son obligatorios",
          "title": ""
        });
      }
      else {
        $.ajax({
          "data": {
            pass,
            "user": userName
          },
          "method": "POST",
          "url": `${BASE.url}login/`
        }).done((err) => {
          let color = "warning";
          if (err.error === true) {
            color = "warning";
          }
          else {
            color = "success";
          }
          $.gritter.add({
            "class_name": `color ${color}`,
            "sticky": false,
            "text": err.message,
            "title": ""
          });
          if (color === "success") {
            redirector = function redirector () {
              $window.location = `${BASE.url}dashboard`;
            };
            const TIMEOUT = 2000;
            $timeout(redirector, TIMEOUT);
          }
        });
      }
    };
  }
);
