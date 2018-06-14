/* eslint no-magic-numbers:
["error", { "ignore": [-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "$state","response"] }]*/
/* global
BASE, document, $, $msg, userName, integrates, userEmail, userName, Rollbar,
mixPanelDashboard, userRole, findingType, actor, scenario, authentication,
confidenciality, Organization, resolutionLevel, explotability, availability,
updateEvidencesFiles:true, findingData:true, realiabilityLevel,
updateEvidenceText:true, categories, probabilities, accessVector, integrity,
accessComplexity, projectData:true, eventsData:true, fieldsToTranslate,
keysToTranslate, desc:true, angular, $window, releaseData:true */
/**
 * @file releaseContentCtrl.js
 * @author engineering@fluidattacks.com
 */
/**
 * Controller definition for finding content view.
 * @name releaseContentCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $translate
 * @param {Object} ngNotify
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller("releaseContentCtrl", function
releaseContentCtrl (
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
  tabsFtry
) {
  $scope.detectNivel = function detectNivel () {
    const TIMEOUT = 200;
    $timeout(() => {
      $scope.$digest();
      if ($scope.finding.level === "Detallado") {
        $scope.esDetallado = true;
        findingData.esDetallado = $scope.esDetallado;
      }
      else {
        $scope.esDetallado = false;
        findingData.esDetallado = $scope.esDetallado;
      }
    }, TIMEOUT);
  };
  $scope.acceptRelease = function acceptRelease () {
    functionsFtry4.acceptRelease($scope);
  };
  $scope.rejectRelease = function rejectRelease () {
    functionsFtry4.rejectRelease($scope);
  };
  $scope.goUp = function goUp () {
    angular.element("html, body").animate({"scrollTop": 0}, "fast");
  };
  $scope.hasUrl = function hasUrl (element) {
    if (angular.isDefined(element)) {
      if (element.indexOf("https://") !== -1 ||
          element.indexOf("http://") !== -1) {
        return true;
      }
    }
    return false;
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
    if (eventsData.length === 0 || (eventsData.length > 0 &&
                   eventsData[0].fluidProject.toLowerCase() !==
                   $stateParams.project.toLowerCase())) {
      const reqEventualities = projectFtry.eventualityByName(
        $stateParams.project,
        "Name"
      );
      reqEventualities.then((response) => {
        if (!response.error) {
          if (angular.isUndefined(response.data)) {
            location.reload();
          }
          eventsData = response.data;
        }
        else if (response.message === "Access to project denied") {
          Rollbar.warning("Warning: Access to event denied");
          $msg.error($translate.instant("proj_alerts.access_denied"));
        }
        else {
          Rollbar.warning("Warning: Event not found");
          $msg.error($translate.instant("proj_alerts.eventExist"));
        }
      });
    }
    if (!$scope.isEmpty(findingData) &&
        findingData.data.fluidProject.toLowerCase() ===
        $stateParams.project.toLowerCase() &&
        findingData.data.id === $scope.finding.id) {
      $scope.view.project = false;
      $scope.view.finding = true;
      $scope.finding = findingData.data;
      $scope.header = findingData.header;
      $scope.tabEvidences = findingData.tabEvidences;
      $scope.hasExploit = findingData.hasExploit;
      $scope.exploitURL = findingData.exploitURL;
      $scope.hasRecords = findingData.hasRecords;
      $scope.esDetallado = findingData.esDetallado;
      $scope.hasRelease = findingData.hasRelease;
      if ($scope.isAdmin && !findingData.hasRelease) {
        $scope.releasesButton = true;
      }
      else {
        $scope.releasesButton = false;
      }
      functionsFtry3.loadFindingContent($scope);
    }
    else {
      const req = projectFtry.findingById(id);
      req.then((response) => {
        if (angular.isUndefined(response.data)) {
          location.reload();
        }
        if (!response.error && $stateParams.project.toLowerCase() ===
            response.data.fluidProject.toLowerCase()) {
          findingData.data = response.data;
          $scope.finding = response.data;
          $scope.hasRelease = false;
          if ($scope.finding.suscripcion === "Continua" ||
            $scope.finding.suscripcion === "Concurrente" ||
            $scope.finding.suscripcion === "Si") {
            $scope.isContinuous = true;
          }
          else {
            $scope.isContinuous = false;
          }
          if (angular.isDefined($scope.finding.releaseDate)) {
            $scope.hasRelease = true;
          }
          findingData.hasRelease = $scope.hasRelease;
          if ($scope.isAdmin && !findingData.hasRelease) {
            $scope.releasesButton = true;
          }
          else {
            $scope.releasesButton = false;
          }
          functionsFtry3.loadFindingContent($scope);
          functionsFtry3.findingHeaderBuilding($scope, findingData);
          findingData.remediated = $scope.isRemediated;
          $scope.view.project = false;
          $scope.view.finding = true;
          const evidenceInfo = tabsFtry.findingEvidenceTab($scope);
          $scope.tabEvidences = evidenceInfo;
          findingData.tabEvidences = evidenceInfo;
          const infoIndex2 = 2;
          const infoIndex3 = 3;
          const exploitinfo =
                             tabsFtry.findingExploitTab($scope, findingData);
          $scope.hasExploit = exploitinfo[0];
          $scope.exploitURL = exploitinfo[1];
          findingData.hasExploit = exploitinfo[infoIndex2];
          findingData.exploitURL = exploitinfo[infoIndex3];
          const recordinfo = tabsFtry.findingRecordsTab($scope, findingData);
          $scope.hasRecords = recordinfo[0];
          findingData.hasRecords = recordinfo[1];
          return true;
        }
        else if (response.error) {
          $scope.view.project = false;
          $scope.view.finding = false;
          if (response.message === "Project masked") {
            Rollbar.warning("Warning: Project deleted");
            $msg.error($translate.instant("proj_alerts.project_deleted"));
          }
          else {
            $msg.error($translate.instant("proj_alerts.no_finding"));
            Rollbar.warning("Warning: Finding not found");
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
  $scope.findingCalculateCSSv2 = function findingCalculateCSSv2 () {
    const cssv2Info = functionsFtry2.findingCalculateCSSv2($scope);
    $scope.finding.cssv2base = cssv2Info[0];
    $scope.finding.criticity = cssv2Info[1];
  };
  $scope.capitalizeFirstLetter = function capitalizeFirstLetter (string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };
  $scope.goBack = function goBack () {
    $scope.view.project = true;
    $scope.view.finding = false;
    projectData = [];
    releaseData = [];
    $state.go("ProjectReleases", {"project": $scope.project});
    angular.element("html, body").animate(
      {"scrollTop": $scope.currentScrollPosition},
      "fast"
    );
  };
  $scope.urlReleaseDescription = function urlReleaseDescription () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/description`);
  };
  $scope.urlReleaseSeverity = function urlReleaseSeverity () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/severity`);
  };
  $scope.urlReleaseEvidence = function urlReleaseEvidence () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/evidence`);
  };
  $scope.urlReleaseExploit = function urlReleaseExploit () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/exploit`);
  };
  $scope.urlReleaseRecords = function urlReleaseRecords () {
    location.replace(`${$window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/records`);
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
    // Flags for editable fields activation
    $scope.onlyReadableTab1 = true;
    $scope.onlyReadableTab2 = true;
    $scope.onlyReadableTab3 = true;
    $scope.onlyReadableTab4 = true;
    $scope.onlyReadableTab5 = true;
    $scope.onlyReadableTab6 = true;
    $scope.isManager = userRole !== "customer" && userRole !== "customeradmin";
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
      functionsFtry2.activeTab("#info", "ReleaseDescription", org, projt, idF);
    }
    if ($window.location.hash.indexOf("severity") !== -1) {
      functionsFtry2.activeTab("#cssv2", "ReleaseSeverity", org, projt, idF);
    }
    if ($window.location.hash.indexOf("evidence") !== -1) {
      functionsFtry2.activeTab("#evidence", "ReleaseEvidence", org, projt, idF);
    }
    if ($window.location.hash.indexOf("exploit") !== -1) {
      functionsFtry2.activeTab(
        "#exploit", "ReleaseExploit",
        org, projt, idF
      );
    }
    if ($window.location.hash.indexOf("records") !== -1) {
      functionsFtry2.activeTab("#records", "ReleaseRecords", org, projt, idF);
      const recordinfo = tabsFtry.findingRecordsTab($scope, findingData);
      $scope.hasRecords = recordinfo[0];
      findingData.hasRecords = recordinfo[1];
    }
  };
  $scope.init();
});
