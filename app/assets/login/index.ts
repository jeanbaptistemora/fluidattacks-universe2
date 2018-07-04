// This file should not be renamed
/* eslint-disable angular/file-name */
/* eslint-disable angular/window-service */
// Login page is isolated from the rest of the application.
/* eslint-disable angular/component-limit*/
/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global angular,$, $timeout, $window */
/**
 * @file index.ts
 */
/*
 *  Set absolute route for Integrates.
 */
import Mixpanel from "mixpanel-browser";
import angular from "angular";


const BASE = {
  "development": "/",
  "isProduction": false,
  "production": "/integrates/",
  "url": ""
};
BASE.isProduction = window.location.
  toString().indexOf("localhost:8000") === -1;

// eslint-disable-next-line angular/window-service
if (window.location.pathname.indexOf("/integrates") === -1) {
  BASE.url = BASE.development;
}
else {
  BASE.url = BASE.production;
}

// Module definition
angular.module("FluidIntegrates", [
  "ngSanitize",
  "cgNotify",
  "pascalprecht.translate"
]);

angular.module("FluidIntegrates").config([
  "$translateProvider",

  /*
   * Angular module configuration only can
   * be made with parameter array injection
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

/**
 * Controller definition for the login view.
 * @name loginCtrl
 * @param {Object} $scope
 * @param {integrates.loginFactory} loginFactory
 * @return {undefined}
 */
angular.module("FluidIntegrates").controller(
  "loginCtrl",
  function loginCtrl (
    $scope,
    $translate,
    $window,
    notify
  ) {
    $scope.init = () => {
      $scope.mixpanel = Mixpanel.init("7a7ceb75ff1eed29f976310933d1cc3e");
      $scope.socialURL = {
        "azure": "",
        "google": ""
      };
      $scope.doubleAuthFactor();
    };

    $scope.google2Factor = () => {
      if (BASE.isProduction) {
        Mixpanel.track("Click Google 2 factor");
      }
    };

    $scope.azure2Factor = () => {
      if (BASE.isProduction) {
        Mixpanel.track("Click Azure 2 factor");
      }
    };

    $scope.doubleAuthFactor = () => {
      const alertTpl =
                `<div>${$translate.instant("login_recommend")}<br><br><div ` +
                "class=\"text-center\"><a class=\"btn btn-danger google " +
                "login-button\" href=\"http://bit.ly/2Gpjt6h\" " +
                "ng-click=\"google2Factor();\" " +
                "target=\"_blank\"><i class=\"fa fa-google-plus fa-2x " +
                "pull-left\" aria-hidden=\"true\"></i></a>" +
                "<a class=\"btn btn-primary azure btn-azure\" " +
                "ng-click=\"azure2Factor()\" " +
                "href=\"http://bit.ly/2Gp1L2X\" target=\"_blank\"><img " +
                "src=\"assets/img/azure.png\" class=\"fa fa-azure " +
                "fa-2x pull-left\" aria-hidden=\"true\" height=\"25\">" +
                "</img></a></div></div>";
      notify({
        "classes": "alert alert-info",
        "duration": 5000,
        "messageTemplate": alertTpl,
        "position": "right",
        "scope": $scope
      });
    };

    $scope.lang = (langKey) => {
      if (langKey === "es" || langKey === "en") {
        localStorage.lang = langKey;
        location.reload();
      }
      $translate.use(localStorage.lang);
    };

    $scope.google = () => {
        Mixpanel.track("Login Google");
      if (BASE.isProduction) {
        Mixpanel.track("Login Google");
      }
      $window.location.href = $scope.socialURL.google;
    };

    $scope.azure = () => {
      if (BASE.isProduction) {
        Mixpanel.track("Login Azure");
      }
      $window.location.href = $scope.socialURL.azure;
    };

    $scope.init();
  }
);
