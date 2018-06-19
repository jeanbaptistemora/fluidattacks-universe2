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
  function dashboardCtrl (
    $scope,
    $state,
    $stateParams,
    $timeout,
    $translate,
    $uibModal,
    $window
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
      location.reload();
    };
  }
);
