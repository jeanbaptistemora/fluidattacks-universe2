/* global
integrates, BASE, userEmail, mixpanel, projectData:true,
eventsData:true, findingData:true
*/
/* eslint no-shadow: ["error", { "allow": ["$scope"] }]*/
/**
 * @file registerCtrl.js
 * @author engineering@fluidattacks.com
 */
/**
 * Crea el controlador de las funciones del registro
 * @name registerController
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @return {undefined}
 */
/** @export */
integrates.controller("registerCtrl", function dashboardCtrl (
  $scope, $uibModal, $timeout,
  $state, $stateParams, $q,
  $translate
) {
  $scope.logout = function logout () {
    const modalInstance = $uibModal.open({
      "animation": true,
      "controller" ($scope, $uibModalInstance) {
        $scope.closeModalLogout = function closeModalLogout () {
          $uibModalInstance.close();
        };
        $scope.okModalLogout = function okModalLogout () {
          projectData = [];
          eventsData = [];
          findingData = {};
          window.location = `${BASE.url}logout`;
        };
      },
      "resolve": {"done": true},
      "templateUrl": "logout.html",
      "windowClass": "modal avance-modal"
    });
  };

  /**
   * Cambia el lenguaje del dashboard
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
});
