/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global angular,$, setTimeout,redirector:true */
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
if (window.location.pathname.indexOf("/integrates") === -1) {
  BASE.url = BASE.development;
}
// Definicion de modulos
const integrates = angular.module("FluidIntegrates", [
  "ngSanitize",
  "pascalprecht.translate"
]);

integrates.config([
  "$translateProvider",
  function config ($translateProvider) {
    const translations = {
      "button": {
        "azure": "Log in with Azure/Office365",
        "google": "Log in with Google"
      },
      "login_message": "Please log in to proceed.",
      "login_welcome": "If you are a new user, you must call a " +
                       "FLUID representative to register."
    };
    const traducciones = {
      "button": {
        "azure": "Ingresar con Azure/Office365",
        "google": "Ingresar con Google"
      },
      "login_message": "Porfavor ingrese.",
      "login_welcome": "Si eres un usuario nuevo, debes llamar a tu " +
                       "representante de FLUID para registrarte"
    };
    $translateProvider.useSanitizeValueStrategy("sanitize");
    $translateProvider.
      translations("en", translations).
      translations("es", traducciones).
      preferredLanguage("en");
  }
]);

/*
 * MixPanel localhost Fixer
 */
integrates.isProduction = function isProduction () {
  return window.location.toString().indexOf("localhost:8000") === -1;
};

/**
 * Crea el controlador de la funcionalidad de autenticacion
 * @name loginController
 * @param {Object} $scope
 * @param {integrates.loginFactory} loginFactory
 * @return {undefined}
 */
integrates.controller("loginController", ($scope, $translate) => {
  $scope.lang = function lang (langKey) {
    if (langKey === "es" || langKey === "en") {
      localStorage.lang = langKey;
    }
    $translate.use(localStorage.lang);
  };

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
            window.location = `${BASE.url}dashboard`;
          };
          const TIMEOUT = 2000;
          setTimeout(redirector, TIMEOUT);
        }
      });
    }
  };
});
