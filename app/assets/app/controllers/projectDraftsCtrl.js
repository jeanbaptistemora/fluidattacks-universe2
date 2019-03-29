/* eslint-disable max-lines */
/* eslint no-magic-numbers: ["error", { "ignore":[-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow":
                                   ["$scope","$stateParams", "projectFtry"] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, draftData:true,
nonexploitLabel:true, totalHigLabel:true, $scope:true,exploitable:true, i:true,
totalSegLabel:true, openLabel:true, partialLabel:true, $msg, integrates, j:true,
document, userName, userEmail, Rollbar, aux:true, json:true, eventsData:true, $,
closeLabel:true, mixPanelDashboard, win:true, window, Organization, userRole,
fieldsToTranslate, keysToTranslate, removeHour:true, labelState:true, angular,
$window */
/**
 * @file projectDraftsCtrl.js
 * @author engineering@fluidattacks.com
 */

/**
 * Controller definition for finding tab view.
 * @name projectDraftsCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "projectDraftsCtrl",
  function projectDraftsCtrl (
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
    projectFtry,
    projectFtry2
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
          "ProjectDrafts",
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
    $scope.goUp = function goUp () {
      angular.element("html, body").animate({"scrollTop": 0}, "fast");
    };
    $scope.search = function search () {
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
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

        if (draftData.length > 0 &&
            draftData[0].projectName.toLowerCase() ===
            $scope.project.toLowerCase()) {
          $scope.view.project = true;
          $scope.loadDraftContent(draftData, vlang);
        }
        else {
          const reqDrafts = projectFtry2.draftsByName(
            projectName,
            tableFilter
          );
          reqDrafts.then((response) => {
            $scope.view.project = true;
            if (!response.error) {
              if (angular.isUndefined(response.data)) {
                location.reload();
              }
              draftData = response.data;
              $scope.loadDraftContent(draftData, vlang);
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
    $scope.goToDraft = function goToDraft (rowInfo) {
      // Mixpanel tracking
      mixPanelDashboard.trackFinding("ReadDraft", userEmail, rowInfo.id);
      $scope.currentScrollPosition = angular.element(document).scrollTop();
      $state.go("FindingDescription", {
        "id": rowInfo.id,
        "project": rowInfo.projectName.toLowerCase()
      });
    };
    $scope.loadDraftContent = function loadDraftContent (datatest) {
      const org = Organization.toUpperCase();
      const projt = $stateParams.project.toUpperCase();
      functionsFtry1.alertHeader(org, projt);
      for (let cont = 0; cont < datatest.length; cont++) {
        for (let inc = 0; inc < fieldsToTranslate.length; inc++) {
          if (datatest[cont][fieldsToTranslate[inc]] in keysToTranslate) {
            datatest[cont][fieldsToTranslate[inc]] =
                  $translate.instant(keysToTranslate[
                    datatest[cont][fieldsToTranslate[inc]]
                  ]);
          }
        }
      }
      // Drafts table configuration
      $scope.tblDraftsHeaders = [
        {
          "align": "center",
          "dataField": "reportDate",
          "header": $translate.instant("search_findings.headings.timestamp"),
          "isDate": true,
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
          "dataField": "exploitable",
          "header": $translate.instant("search_findings.headings.exploit"),
          "width": "6%"
        },
        {
          "align": "center",
          "dataField": "releaseStatus",
          "header": $translate.instant("search_findings.headings.released"),
          "width": "6%"
        }
      ];
      $scope.draftsDataset = datatest;
      angular.element("#search_section").show();
      angular.element("[data-toggle=\"tooltip\"]").tooltip();

      if (angular.isDefined($stateParams.finding)) {
        $scope.finding.id = $stateParams.finding;
        $scope.view.project = false;
        $scope.view.finding = false;
      }
      $scope.data = datatest;
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
