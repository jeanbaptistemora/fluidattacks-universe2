/* eslint-disable angular/document-service */
/* eslint no-magic-numbers: ["error", { "ignore":[-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow":
                                   ["$scope","$stateParams", "projectFtry"] }]*/
/* global
BASE, integrates, Organization, mixPanelDashboard, userName, userEmail, $,
Rollbar, angular,$window */
/**
 * @file reportGeneratorCtrl.js
 * @author engineering@fluidattacks.com
 */

/**
 * Controller definition for report generator modal.
 * @name reportGeneratorCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "reportGeneratorCtrl",
  function reportGeneratorCtrl (
    $scope,
    $timeout
  ) {

    $scope.downloadDoc = function downloadDoc () {
      const TIMEOUT = 3000;
      if (angular.isUndefined($scope.downloadURL)) {
        $timeout($scope.downloadDoc, TIMEOUT);
      }
      else {
        const downLink = document.createElement("a");
        downLink.target = "_blank";
        downLink.href = $scope.downloadURL;
        downLink.click();
      }
    };
  }
);
