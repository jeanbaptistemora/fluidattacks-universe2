/* eslint no-shadow: ["error", { "allow": ["$scope"] }]*/
/* eslint no-magic-numbers: ["error", { "ignore":[-1,0,1] }]*/
/* eslint lines-around-comment: [2, { "beforeBlockComment": false }]*/
/* global
integrates, $,   mixpanel, userMail, $xhr, Organization, userEmail, angular,
mixPanelDashboard, userName, projectData:true, eventsData:true, Rollbar, BASE,
findingData:true, fieldsToTranslate, keysToTranslate, modalInstance:true, $msg,
$window */
/**
 * @file navbarCtrl.js
 * @author engineering@fluidattacks.com
 */
/**
 * Controller definition for the navigation bar.
 * @name navbarController
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "navbarCtrl",
  function navbarCtrl (
    $scope,
    $uibModal,
    $window
  ) {
    /**
     * Redirect a user to the logout view.
     * @function logout
     * @member integrates.navbarCtrl
     * @return {undefined}
     */
    $scope.logout = function logout () {
      $uibModal.open({
        "animation": true,
        "backdrop": "static",
        "controller" ($scope, $uibModalInstance) {
          $scope.closeModalLogout = function closeModalLogout () {
            $uibModalInstance.close();
          };
          $scope.okModalLogout = function okModalLogout () {
            projectData = [];
            eventsData = [];
            findingData = {};
            let org = "";
            try {
              org = Organization.toUpperCase();
            }
            catch (err) {
              org = "undefined";
            }
            mixPanelDashboard.trackSessionLength(
              userName,
              userEmail,
              org
            );
            localStorage.clear();
            $window.location = `${BASE.url}logout`;
          };
        },
        "keyboard": false,
        "resolve": {"done": true},
        "templateUrl": "logout.html",
        "windowClass": "modal avance-modal"
      });
    };
  }
);
