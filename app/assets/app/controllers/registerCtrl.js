/* eslint no-magic-numbers: ["error", { "ignore":[-1,0,1] }]*/
/* global
integrates, BASE, userEmail, mixpanel, projectData:true,
eventsData:true, findingData:true, angular, $window, Rollbar */
/* eslint no-shadow: ["error", { "allow": ["$scope"] }]*/
/**
 * @file registerCtrl.js
 * @author engineering@fluidattacks.com
 */
/**
 * Controller definition for user registration view.
 * @name registerController
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "registerCtrl",
  function registerCtrl (
    $scope,
    $state,
    $stateParams,
    $timeout,
    $translate,
    $uibModal,
    $window,
    registerFactory
  ) {
    $scope.loadDashboard = function loadDashboard () {
      const currentUrl = $window.location.toString();
      if (localStorage.getItem("url_inicio") === null) {
        $window.location = "dashboard";
      }
      else {
        let baseUrl = "";
        if (currentUrl.indexOf("localhost:8000") === -1) {
          if (currentUrl.indexOf(".integrates.env") === -1) {
            baseUrl = "https://fluidattacks.com/integrates/dashboard";
            const link = `${baseUrl}#${localStorage.getItem("url_inicio")}`;
            localStorage.removeItem("url_inicio");
            $window.location = link;
          }
          else {
            const dev = currentUrl.match("https://(.*).integrates")[1];
            baseUrl = `https://${dev}.integrates.env.fluidattacks.com/dashbo`;
            const link = `${baseUrl}ard#${localStorage.getItem("url_inicio")}`;
            localStorage.removeItem("url_inicio");
            $window.location = link;
          }
        }
        else {
          baseUrl = "https://localhost:8000/dashboard";
          const link = `${baseUrl}#${localStorage.getItem("url_inicio")}`;
          localStorage.removeItem("url_inicio");
          $window.location = link;
        }
      }
    };

    $scope.initLegalNotice = function initLegalNotice () {
      $scope.alreadyLoggedIn = false;
      const translationStrings = [
        "legalNotice.acceptBtn.text",
        "legalNotice.acceptBtn.tooltip",
        "legalNotice.rememberCbo.text",
        "legalNotice.rememberCbo.tooltip",
        "legalNotice.description",
        "legalNotice.title"
      ];
      $scope.translations = {};
      angular.forEach(translationStrings, (value) => {
        $scope.translations[value] = $translate.instant(value);
      });
      const infoReq = registerFactory.getLoginInfo();
      infoReq.then((response) => {
        const respData = response.data;
        if (angular.isUndefined(respData)) {
          location.reload();
        }
        else if (!respData.login.authorized) {
          $scope.isAuthorized = false;
          const currentUrl = $window.location.toString();
          if (currentUrl.indexOf("localhost:8000") === -1) {
            mixpanel.track("Registered User", {
              "Email":
              "{{ request.session.username }}"
            });
          }
        }
        else if (respData.login.remember) {
          $scope.loadDashboard();
        }
        else {
          $scope.showLegalNotice = true;
        }
      });
    };

    $scope.init = function init () {
      $scope.showLegalNotice = false;
      $scope.isAuthorized = true;
      if (localStorage.getItem("showAlreadyLoggedin") === "1") {
        const TIMEOUT = 200;
        $timeout(() => {
          angular.element("#full_loader").hide();
        }, TIMEOUT);
        $scope.alreadyLoggedIn = true;
        localStorage.removeItem("showAlreadyLoggedin");
      }
      else {
        $scope.initLegalNotice();
      }
    };

    $scope.init();
  }
);
