/* eslint-disable max-lines */
/* eslint no-magic-numbers: ["error", { "ignore":[-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow":
                                   ["$scope","$stateParams", "projectFtry"] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, projectData:true,
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
    $scope.init = function init () {
      const projectName = $stateParams.project;
      const findingId = $stateParams.finding;
      $scope.userRole = userRole;
      functionsFtry4.verifyRoles($scope, projectName, userEmail, userRole);
      // Default flags value for view visualization.
      $scope.view = {};
      $scope.view.project = false;
      $scope.view.finding = false;
      // Route parameters.
      if (angular.isDefined(findingId)) {
        $scope.findingId = findingId;
      }
      if (angular.isDefined(projectName) &&
                projectName !== "") {
        $scope.project = projectName;
        $scope.search();
        const org = Organization.toUpperCase();
        const projt = projectName.toUpperCase();
        mixPanelDashboard.trackReports(
          "ProjectFindings",
          userName,
          userEmail,
          org,
          projt
        );
      }
      // Search function assignation to button and enter key configuration.
      functionsFtry3.configKeyboardView($scope);
      $scope.goUp();
      $scope.finding = {};
    };
    $scope.deleteProject = function deleteProject () {
      functionsFtry4.deleteProject();
    };
    $scope.goUp = function goUp () {
      angular.element("html, body").animate({"scrollTop": 0}, "fast");
    };
    $scope.search = function search () {
      const projectName = $stateParams.project;
      const tableFilter = $scope.filter;
      const hasAccess = true;
      if (angular.isUndefined(projectName) ||
                projectName === "") {
        const attentionAt = $translate.instant("proj_alerts.attentTitle");
        const attentionAc = $translate.instant("proj_alerts.attent_cont");
        $msg.warning(attentionAc, attentionAt);
        return false;
      }
      if ($stateParams.project !== $scope.project) {
        $state.go("ProjectIndicators", {"project": $scope.project});
      }
      else if ($stateParams.project === $scope.project) {
        $scope.view.project = false;
        $scope.view.finding = false;

        if (projectData.length > 0 &&
            projectData[0].projectName.toLowerCase() ===
            $scope.project.toLowerCase()) {
          $scope.view.project = true;
          $scope.loadFindingContent(projectData);
        }
        else {
          const reqProject = projectFtry.projectByName(
            projectName,
            tableFilter
          );
          reqProject.then((response) => {
            $scope.view.project = true;
            if (!response.error) {
              if (angular.isUndefined(response.data)) {
                location.reload();
              }
              else {
                // Mixpanel tracking
                mixPanelDashboard.trackSearch(
                  "SearchFinding",
                  userEmail,
                  projectName
                );
                projectData = response.data;
                $scope.loadFindingContent(projectData);
              }
            }
            else if (response.error) {
              $scope.view.project = false;
              $scope.view.finding = false;
              if (response.message === "Access denied" || !hasAccess) {
                $msg.error($translate.instant("proj_alerts.access_denied"));
              }
              else if (response.message === "Project masked") {
                $msg.error($translate.instant("proj_alerts.project_deleted"));
              }
              else {
                $msg.error($translate.instant("proj_alerts.error_text"));
              }
            }
          });
        }
      }
      return true;
    };
    $scope.goToFinding = function goToFinding (rowInfo) {
      // Mixpanel tracking
      mixPanelDashboard.trackFinding("ReadFinding", userEmail, rowInfo.id);
      $scope.currentScrollPosition = angular.element(document).scrollTop();
      $state.go("FindingDescription", {
        "id": rowInfo.id,
        "project": rowInfo.projectName.toLowerCase()
      });
    };
    $scope.loadFindingContent = function loadFindingContent (datatest) {
      const org = Organization.toUpperCase();
      const projt = $stateParams.project.toUpperCase();
      functionsFtry1.alertHeader(org, projt);
      for (let cont = 0; cont < datatest.length; cont++) {
        if ("openVulnerabilities" in datatest[cont]) {
          datatest[cont].openVulnerabilities =
            parseInt(datatest[cont].openVulnerabilities, 10);
        }
        for (let inc = 0; inc < fieldsToTranslate.length; inc++) {
          if (datatest[cont][fieldsToTranslate[inc]] in keysToTranslate) {
            datatest[cont][fieldsToTranslate[inc]] =
                  $translate.instant(keysToTranslate[
                    datatest[cont][fieldsToTranslate[inc]]
                  ]);
          }
        }
      }
      // Findings table configuration
      $scope.tblFindingsHeaders = [
        {
          "align": "center",
          "dataField": "edad",
          "header": $translate.instant("search_findings.headings.age"),
          "width": "4.8%"
        },
        {
          "align": "center",
          "dataField": "lastVulnerability",
          "header":
            $translate.instant("search_findings.headings.lastVulnerability"),
          "width": "4.8%"
        },
        {
          "align": "center",
          "dataField": "findingType",
          "header": $translate.instant("search_findings.headings.type"),
          "width": "6.5%"
        },
        {
          "align": "left",
          "dataField": "finding",
          "header": $translate.instant("search_findings.headings.finding"),
          "width": "6%",
          "wrapped": true
        },
        {
          "align": "left",
          "dataField": "vulnerability",
          "header":
            $translate.instant("search_findings.headings.vulnerability"),
          "width": "13%",
          "wrapped": true
        },
        {
          "align": "center",
          "dataField": "criticity",
          "header": $translate.instant("search_findings.headings.criticity"),
          "width": "5.5%"
        },
        {
          "align": "center",
          "dataField": "openVulnerabilities",
          "header": $translate.instant("search_findings.headings.cardinality"),
          "width": "5%"
        },
        {
          "align": "center",
          "dataField": "estado",
          "header": $translate.instant("search_findings.headings.state"),
          "isStatus": true,
          "width": "10.5%"
        },
        {
          "align": "center",
          "dataField": "treatment",
          "header": $translate.instant("search_findings.headings.treatment"),
          "width": "6%"
        },
        {
          "align": "center",
          "dataField": "exploitable",
          "header": $translate.instant("search_findings.headings.exploit"),
          "width": "6%"
        }
      ];
      $scope.findingsDataset = datatest;
      angular.element("#search_section").show();
      angular.element("[data-toggle=\"tooltip\"]").tooltip();

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
