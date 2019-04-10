/* eslint-disable max-lines */
/* eslint no-magic-numbers: ["error", { "ignore":[-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow":
                                   ["$scope","$stateParams", "projectFtry"] }]*/
/* global
BASE, downLink:true, estado:true, exploitLabel:true, projectData:true,
nonexploitLabel:true, totalHigLabel:true, $scope:true,exploitable:true, i:true,
totalSegLabel:true, openLabel:true, partialLabel:true, $msg, integrates, j:true,
document, userName, userEmail, Rollbar, aux:true, json:true, eventsData:true, $,
closeLabel:true, mixPanelDashboard, win:true, window, Organization, userRole,
fieldsToTranslate, keysToTranslate, removeHour:true, labelState:true, angular,
$window */
/**
 * @file projectFindingsCtrl.js
 * @author engineering@fluidattacks.com
 */
/**
 * @function removeHour
 * @param {string} value Date of the finging with hour
 * @member integrates.registerCtrl
 * @return {string} Date without hour
 */
/* eslint-disable-next-line  func-name-matching */
removeHour = function removeHourFunction (value) {
  if (value.indexOf(":") !== -1) {
    return value.split(" ")[0];
  }
  return value;
};

/**
 * @function labelState
 * @param {string} value Status of the finding
 * @member integrates.registerCtrl
 * @return {string} Html code for specific label
 */

/**
 * Controller definition for finding tab view.
 * @name ProjectCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "projectFindingsCtrl",
  function projectFindingsCtrl (
    $location,
    $scope,
    $state,
    $stateParams,
    $timeout,
    $translate,
    $uibModal,
    $window,
    functionsFtry1,
    functionsFtry3,
    functionsFtry4,
    projectFtry
  ) {
    $scope.loadFindingContent = function loadFindingContent (datatest) {
      if (angular.isDefined($stateParams.finding)) {
        $scope.finding.id = $stateParams.finding;
        $scope.view.project = false;
        $scope.view.finding = false;
      }
      if (!$scope.isManager) {
        $scope.openEvents = projectFtry.alertEvents(eventsData);
        $scope.atAlert = $translate.instant("main_content.eventualities." +
                                            "descSingularAlert1");
        if ($scope.openEvents === 1) {
          $scope.descAlert1 = $translate.instant("main_content.eventualities." +
                                                  "descSingularAlert2");
          $scope.descAlert2 = $translate.instant("main_content.eventualities." +
                                                  "descSingularAlert3");
          angular.element("#events_alert").show();
        }
        else if ($scope.openEvents > 1) {
          $scope.descAlert1 = $translate.instant("main_content.eventualities." +
                                                  "descPluralAlert1");
          $scope.descAlert2 = $translate.instant("main_content.eventualities." +
                                                  "descPluralAlert2");
          angular.element("#events_alert").show();
        }
      }
    };
    $scope.init();
  }
);
