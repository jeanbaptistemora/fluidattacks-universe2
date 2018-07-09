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
  projectFtry2,
  tabsFtry
) {
  $scope.cssv2Editable = function cssv2Editable () {
    if ($scope.onlyReadableTab2 === false) {
      $scope.onlyReadableTab2 = true;
    }
    else {
      $scope.onlyReadableTab2 = false;
    }
  };
  $scope.descriptionEditable = function descriptionEditable () {
    if ($scope.onlyReadableTab1 === false) {
      $scope.onlyReadableTab1 = true;
    }
    else {
      $scope.onlyReadableTab1 = false;
    }
  };
  $scope.treatmentEditable = function treatmentEditable () {
    functionsFtry1.treatmentEditable($scope);
  };
  $scope.evidenceEditable = function evidenceEditable () {
    functionsFtry2.evidenceEditable($scope);
  };
  $scope.exploitEditable = function exploitEditable () {
    functionsFtry2.exploitEditable($scope);
  };
  $scope.recordsEditable = function recordsEditable () {
    functionsFtry2.recordsEditable($scope);
  };
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
  $scope.updateCSSv2 = function updateCSSv2 () {
    functionsFtry1.updateCSSv2($scope);
  };
  updateEvidencesFiles = function updateEvidencesFiles (element) {
    functionsFtry2.updateEvidencesFiles(element, $scope);
  };
  updateEvidenceText = function updateEvidenceText (element) {
    functionsFtry1.updateEvidenceText(element, $scope);
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
      $scope.isRemediated = findingData.remediated;
      $scope.tabEvidences = findingData.tabEvidences;
      $scope.hasExploit = findingData.hasExploit;
      $scope.exploitURL = findingData.exploitURL;
      $scope.hasRecords = findingData.hasRecords;
      $scope.esDetallado = findingData.esDetallado;
      $scope.hasDraft = findingData.hasDraft;
      if ($scope.isAdmin && !findingData.hasDraft) {
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
            response.data.fluidProject.toLowerCase()) {
          findingData.data = response.data;
          $scope.finding = response.data;
          $scope.hasDraft = false;
          if ($scope.finding.suscripcion === "Continua" ||
            $scope.finding.suscripcion === "Concurrente" ||
            $scope.finding.suscripcion === "Si") {
            $scope.isContinuous = true;
          }
          else {
            $scope.isContinuous = false;
          }
          if (angular.isDefined($scope.finding.releaseDate)) {
            $scope.hasDraft = true;
          }
          findingData.hasDraft = $scope.hasDraft;
          if ($scope.isAdmin && !findingData.hasDraft) {
            $scope.draftsButton = true;
          }
          else {
            $scope.draftsButton = false;
          }
          functionsFtry3.loadFindingContent($scope);
          functionsFtry3.findingHeaderBuilding($scope, findingData);
          $scope.remediatedView();
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
  $scope.remediatedView = function remediatedView () {
    $scope.isManager = userRole !== "customer" && userRole !== "customeradmin";
    $scope.isRemediated = true;
    if (angular.isDefined($scope.finding.id)) {
      const req = projectFtry.remediatedView($scope.finding.id);
      req.then((response) => {
        if (!response.error) {
          $scope.isRemediated = response.data.remediated;
          findingData.remediated = $scope.isRemediated;
          if ($scope.isManager && $scope.isRemediated) {
            angular.element(".finding-verified").show();
          }
          else {
            angular.element(".finding-verified").hide();
          }
        }
        else if (response.error) {
          Rollbar.error("Error: An error occurred when " +
                        "remediating/verifying the finding");
        }
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
  $scope.updateDescription = function updateDescription () {
    functionsFtry3.updateDescription($scope);
  };
  $scope.findingSolved = function findingSolved () {
    functionsFtry3.findingSolved($scope);
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
  $scope.updateTreatment = function updateTreatment () {
    functionsFtry1.updateTreatment($scope);
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
      functionsFtry2.activeTab("#info", "FindingDescription", org, projt, idF);
    }
    if ($window.location.hash.indexOf("severity") !== -1) {
      functionsFtry2.activeTab("#cssv2", "FindingSeverity", org, projt, idF);
    }
    if ($window.location.hash.indexOf("tracking") !== -1) {
      functionsFtry2.activeTab("#tracking", "FindingTracking", org, projt, idF);
    }
    if ($window.location.hash.indexOf("evidence") !== -1) {
      functionsFtry2.activeTab("#evidence", "FindingEvidence", org, projt, idF);
    }
    if ($window.location.hash.indexOf("exploit") !== -1) {
      functionsFtry2.activeTab(
        "#exploit", "FindingExploit",
        org, projt, idF
      );
    }
    if ($window.location.hash.indexOf("records") !== -1) {
      functionsFtry2.activeTab("#records", "FindingRecords", org, projt, idF);
      const recordinfo = tabsFtry.findingRecordsTab($scope, findingData);
      $scope.hasRecords = recordinfo[0];
      findingData.hasRecords = recordinfo[1];
    }
    if ($window.location.hash.indexOf("comments") !== -1) {
      functionsFtry2.activeTab("#comment", "FindingComments", org, projt, idF);
      tabsFtry.findingCommentTab($scope, $stateParams, "comment");
    }
    if ($window.location.hash.indexOf("observations") !== -1) {
      functionsFtry2.
        activeTab("#observations", "FindingObservations", org, projt, idF);
      tabsFtry.findingCommentTab($scope, $stateParams, "observation");
    }
  };
  $scope.init();
});
