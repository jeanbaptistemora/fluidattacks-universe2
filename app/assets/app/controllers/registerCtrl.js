/* eslint no-magic-numbers: ["error", { "ignore":[-1,0,1] }]*/
/* global
integrates, BASE, userEmail, mixpanel, projectData:true,
eventsData:true, findingData:true, angular, $window */
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
    $scope.logout = function logout () {
      $uibModal.open({
        "animation": true,
        "controller" ($scope, $uibModalInstance) {
          $scope.closeModalLogout = function closeModalLogout () {
            $uibModalInstance.close();
          };
          $scope.okModalLogout = function okModalLogout () {
            projectData = [];
            eventsData = [];
            findingData = {};
            mixpanel.track("Logged out");
            $window.location = `${BASE.url}logout`;
          };
        },
        "resolve": {"done": true},
        "templateUrl": "logout.html",
        "windowClass": "modal avance-modal"
      });
    };

    /**
     * Change the language of the user registration view.
     * @function changeLang
     * @param {string} langKey Language key set by the user
     * @member integrates.registerCtrl
     * @return {undefined}
     */
    $scope.changeLang = function changeLang (langKey) {
      if (langKey === "es" || langKey === "en") {
        localStorage.lang = langKey;
      }
      $translate.use(localStorage.lang);
      mixpanel.identify(userEmail);
      mixpanel.people.set({"$Language": localStorage.lang});
      $window.location.reload();
    };

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
            localStorage.clear();
            $window.location = link;
          }
          else {
            const dev = currentUrl.match("https://(.*).integrates")[1];
            baseUrl = `https://${dev}.integrates.env.fluidattacks.com/dashbo`;
            const link = `${baseUrl}ard#${localStorage.getItem("url_inicio")}`;
            localStorage.clear();
            $window.location = link;
          }
        }
        else {
          baseUrl = "https://localhost:8000/dashboard";
          const link = `${baseUrl}#${localStorage.getItem("url_inicio")}`;
          localStorage.clear();
          $window.location = link;
        }
      }
    };

    $scope.showLegalNotice = function showLegalNotice () {
      $uibModal.open({
        "animation": true,
        "backdrop": "static",
        "controller" ($scope, $uibModalInstance) {
          $scope.okModalNotice = function okModalNotice () {
            const authorizationReq = registerFactory.isUserRegistered();
            authorizationReq.then((response) => {
              if (response.message === "1") {
                mixpanel.time_event("Logged out");
                const statusReq = registerFactory.updateLegalStatus("1");
                statusReq.then(() => {
                  $scope.loadDashboard();
                });
              }
              else {
                angular.element("#notAuthorizedTxt").show();
                $uibModalInstance.close();
                const currentUrl = $window.location.toString();
                if (currentUrl.indexOf("localhost:8000") === -1) {
                  mixpanel.track("Registered User", {
                    "Email":
                  "{{ request.session.username }}"
                  });
                }
              }
            });
          };
        },
        "keyboard": false,
        "resolve": {"done": true},
        "scope": $scope,
        "templateUrl": "legalNotice.html",
        "windowClass": "modal avance-modal"
      });
    };
    $scope.showLegalNotice();
  }
);
