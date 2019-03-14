/* eslint no-magic-numbers:
["error", { "ignore": [-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "$state","response"] }]*/
/* global
BASE, document, $, $msg, userName, integrates, userEmail, userName, Rollbar,
mixPanelDashboard, userRole, findingType, actor, scenario, authentication,
confidenciality, Organization, resolutionLevel, explotability, availability,
findingData:true, realiabilityLevel,
categories, probabilities, accessVector, integrity,
accessComplexity, projectData:true, eventsData:true, draftData:true,
fieldsToTranslate, keysToTranslate, desc:true, angular, $window*/
/**
 * @file findingContentCtrl.js
 * @author engineering@fluidattacks.com
 */
/**
 * Controller definition for finding content view.
 * @name findingContentCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $translate
 * @param {Object} ngNotify
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller("findingContentCtrl", function
findingContentCtrl (
  $scope,
  $state,
  $stateParams,
  $timeout,
  $translate,
  $uibModal,
  $window,
  functionsFtry1,
  functionsFtry2,
  functionsFtry3,
  functionsFtry4,
  ngNotify,
  projectFtry,
  projectFtry2
) {
  $scope.goUp = function goUp () {
    angular.element("html, body").animate({"scrollTop": 0}, "fast");
  };
  $scope.isEmpty = function isEmpty (obj) {
    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        return false;
      }
    }
    return true;
  };

  $scope.goBack = function goBack () {
    $scope.view.project = true;
    $scope.view.finding = false;
    projectData = [];
    draftData = [];
    $state.go("ProjectFindings", {"project": $scope.project});
    angular.element("html, body").animate(
      {"scrollTop": $scope.currentScrollPosition},
      "fast"
    );
  };

  $scope.init = function init () {
    const projectName = $stateParams.project;
    const findingId = $stateParams.finding;
    $scope.userRole = userRole;
    const hasAccess = projectFtry2.accessToProject(projectName);
    hasAccess.then((response) => {
      if (!response.error) {
        $scope.hasAccess = response.data;
        $scope.isManager = userRole !== "customer" &&
                           userRole !== "customeradmin";
      }
      else if (response.error) {
        $scope.hasAccess = false;
        $scope.isManager = false;
        $msg.error($translate.instant("proj_alerts.access_denied"));
      }
    });
    // Default flags value for view visualization
    $scope.isAdmin = userRole !== "customer" &&
            userRole !== "customeradmin" && userRole !== "analyst";
    $scope.view = {};
    $scope.view.project = false;
    $scope.view.finding = false;
    // Route parameters
    if (angular.isDefined(findingId)) {
      $scope.findingId = findingId;
    }
    if (angular.isDefined(projectName) &&
            projectName !== "") {
      $scope.project = projectName;
    }
    // Initialization of search findings function
    $scope.finding = {};
    $scope.finding.id = $stateParams.id;
    $scope.goUp();
  };
  $scope.init();
});
