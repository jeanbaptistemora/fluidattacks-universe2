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
  $scope.detectNivel = function detectNivel () {
    const TIMEOUT = 200;
    $timeout(() => {
      $scope.$digest();
      if ($scope.finding.reportLevel === "DETAILED") {
        $scope.esDetallado = true;
        findingData.esDetallado = $scope.esDetallado;
      }
      else {
        $scope.esDetallado = false;
        findingData.esDetallado = $scope.esDetallado;
      }
    }, TIMEOUT);
  };
  $scope.deleteFinding = function deleteFinding () {
    functionsFtry1.deleteFinding($scope);
  };
  $scope.goUp = function goUp () {
    angular.element("html, body").animate({"scrollTop": 0}, "fast");
  };
  $scope.acceptDraft = function acceptDraft () {
    functionsFtry4.acceptDraft($scope);
  };
  $scope.deleteDraft = function deleteDraft () {
    functionsFtry4.deleteDraft($scope);
  };
  $scope.isEmpty = function isEmpty (obj) {
    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        return false;
      }
    }
    return true;
  };
  $scope.loadFindingByID = function loadFindingByID (id) {
    if (!$scope.isEmpty(findingData) &&
        findingData.data.projectName.toLowerCase() ===
        $stateParams.project.toLowerCase() &&
        findingData.data.id === $scope.finding.id) {
      $scope.view.project = false;
      $scope.view.finding = true;
      $scope.finding = findingData.data;
      $scope.header = findingData.header;
      $scope.esDetallado = findingData.esDetallado;
      $scope.hasDraft = findingData.hasDraft;
      if ($scope.isAdmin && findingData.hasDraft) {
        $scope.draftsButton = true;
      }
      else {
        $scope.draftsButton = false;
      }
      functionsFtry3.loadFindingContent($scope);
    }
    else {
      const req = projectFtry.findingById(
        id,
        $stateParams.project.toLowerCase()
      );
      req.then((response) => {
        if (angular.isUndefined(response.data)) {
          location.reload();
        }
        if (!response.error && $stateParams.project.toLowerCase() ===
            response.data.projectName.toLowerCase()) {
          findingData.data = response.data;
          $scope.finding = response.data;
          $scope.hasDraft = false;
          if (angular.isUndefined($scope.finding.releaseDate)) {
            $scope.hasDraft = true;
          }
          findingData.hasDraft = $scope.hasDraft;
          if ($scope.isAdmin && findingData.hasDraft) {
            $scope.draftsButton = true;
          }
          else {
            $scope.draftsButton = false;
          }
          functionsFtry3.loadFindingContent($scope);
          functionsFtry3.findingHeaderBuilding($scope, findingData);
          $scope.view.project = false;
          $scope.view.finding = true;
          return true;
        }
        else if (response.error) {
          $scope.view.project = false;
          $scope.view.finding = false;
          if (response.message === "Project masked") {
            $msg.error($translate.instant("proj_alerts.project_deleted"));
          }
          else {
            $msg.error($translate.instant("proj_alerts.no_finding"));
          }
        }
        return true;
      });
    }
  };

  $scope.configColorPalette = function configColorPalette () {
    $scope.colors = {};
    // Red
    $scope.colors.critical = "background-color: #f12;";
    // Orange
    $scope.colors.moderate = "background-color: #f72;";
    // Yellow
    $scope.colors.tolerable = "background-color: #ffbf00;";
    // Green
    $scope.colors.ok = "background-color: #008000;";
  };
  $scope.capitalizeFirstLetter = function capitalizeFirstLetter (string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };
  $scope.findingVerified = function findingVerified () {
    functionsFtry1.findingVerified($scope);
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
  $scope.urlDescription = function urlDescription () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/description`);
  };
  $scope.urlSeverity = function urlSeverity () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/severity`);
  };
  $scope.urlTracking = function urlTracking () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/tracking`);
  };
  $scope.urlEvidence = function urlEvidence () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/evidence`);
  };
  $scope.urlExploit = function urlExploit () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/exploit`);
  };
  $scope.urlRecords = function urlRecords () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/records`);
  };
  $scope.urlComments = function urlComments () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/comments`);
  };
  $scope.urlObservations = function urlObservations () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/observations`);
  };
  $scope.urlEvents = function urlEvents () {
    $state.go("ProjectEvents", {"project": $stateParams.project});
  };
  $scope.urlUsers = function urlUsers () {
    $state.go("ProjectUsers", {"project": $scope.project});
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
    $scope.currentTab = "description";
    // Route parameters
    if (angular.isDefined(findingId)) {
      $scope.findingId = findingId;
    }
    if (angular.isDefined(projectName) &&
            projectName !== "") {
      $scope.project = projectName;
    }
    // Initialization of search findings function
    $scope.configColorPalette();
    $scope.finding = {};
    $scope.finding.id = $stateParams.id;
    $scope.loadFindingByID($stateParams.id);
    $scope.goUp();
    const org = Organization.toUpperCase();
    const projt = projectName.toUpperCase();
    functionsFtry1.alertHeader(org, projt);
    const idF = $scope.finding.id;
    if ($window.location.hash.indexOf("description") !== -1) {
      $scope.currentTab = "description";
      functionsFtry2.activeTab("#info", "FindingDescription", org, projt, idF);
    }
    if ($window.location.hash.indexOf("severity") !== -1) {
      $scope.currentTab = "severity";
      functionsFtry2.activeTab("#cssv2", "FindingSeverity", org, projt, idF);
    }
    if ($window.location.hash.indexOf("tracking") !== -1) {
      $scope.currentTab = "tracking";
      functionsFtry2.activeTab("#tracking", "FindingTracking", org, projt, idF);
    }
    if ($window.location.hash.indexOf("evidence") !== -1) {
      $scope.currentTab = "evidence";
      functionsFtry2.activeTab("#evidence", "FindingEvidence", org, projt, idF);
    }
    if ($window.location.hash.indexOf("exploit") !== -1) {
      $scope.currentTab = "exploit";
      functionsFtry2.activeTab(
        "#exploit", "FindingExploit",
        org, projt, idF
      );
    }
    if ($window.location.hash.indexOf("records") !== -1) {
      $scope.currentTab = "records";
      functionsFtry2.activeTab("#records", "FindingRecords", org, projt, idF);
    }
    if ($window.location.hash.indexOf("comments") !== -1) {
      $scope.currentTab = "comments";
      functionsFtry2.activeTab("#comment", "FindingComments", org, projt, idF);
    }
    if ($window.location.hash.indexOf("observations") !== -1) {
      $scope.currentTab = "observations";
      functionsFtry2.
        activeTab("#observations", "FindingObservations", org, projt, idF);
    }
  };
  $scope.init();
});
