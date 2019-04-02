/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, i:true, j:true,
nonexploitLabel:true, totalHigLabel:true, exploitable:true, totalSegLabel:true,
openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg,
userName, userEmail, Rollbar, aux:true, json:true, closeLabel:true, angular,
mixPanelDashboard, win:true, Organization, projectData:true, eventsData:true
*/
/* eslint-env node*/
/**
 * @file ProjectCtrl.js
 * @author engineering@fluidattacks.com
 */
/* Table Formatter */

/**
 * Controller definition for indicators tab view.
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
  "projectIndicatorsCtrl",
  function projectIndicatorsCtrl (
    $location,
    $scope,
    $state,
    $stateParams,
    $timeout,
    $translate,
    $uibModal,
    functionsFtry1,
    functionsFtry3,
    functionsFtry4,
    projectFtry
  ) {
    const PERCENT_FACTOR = 100;
    const MAX_DECIMALS = 2;
    $scope.init = function init () {
      const projectName = $stateParams.project;
      const findingId = $stateParams.finding;
      $scope.userRole = userRole;
      functionsFtry4.verifyRoles($scope, projectName, userEmail, userRole);
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
        angular.element(".equalWidgetHeight").matchHeight();
        mixPanelDashboard.trackReports(
          "ProjectIndicators",
          userName,
          userEmail,
          org,
          projt
        );
      }
      // Search function assignation to button and enter key configuration.
      functionsFtry3.configKeyboardView($scope);
      $scope.goUp();
    };

    /**
     *  @name percent
     *  @description calculate percent
     *  @param {int} value Portion or percent
     *  @param {int} total Total value
     *  @return {string} return n% format
     */
    $scope.percent = (value, total) => ` ${
      (value * PERCENT_FACTOR / total).
        toFixed(MAX_DECIMALS).
        toString()}%`;

    $scope.goUp = function goUp () {
      angular.element("html, body").animate({"scrollTop": 0}, "fast");
    };
    $scope.search = function search () {
      const projectName = $scope.project;
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
          functionsFtry4.loadIndicatorsContent($scope, projectData);
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
              mixPanelDashboard.trackSearch(
                "SearchFinding",
                userEmail,
                projectName
              );
              projectData = response.data;
              functionsFtry4.loadIndicatorsContent($scope, projectData);
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
    $scope.init();
  }
);
