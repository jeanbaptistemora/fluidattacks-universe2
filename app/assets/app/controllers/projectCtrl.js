/* eslint no-magic-numbers: ["error",{ "ignore": [-1,0,1] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, win:true, window,
nonexploitLabel:true, totalHigLabel:true, exploitable:true, totalSegLabel:true,
openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg,
userName, userEmail, Rollbar, aux:true, json:true, closeLabel:true, j:true,
mixPanelDashboard, Organization, projectData:true, eventsData:true, i:true,
angular
*/
/**
 * @file ProjectCtrl.js
 * @author engineering@fluidattacks.com
 */
/**
 * Controller definition for project search view.
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
  "projectCtrl",
  function projectCtrl (
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
    $scope.init = function init () {
      const projectName = $stateParams.project;
      const findingId = $stateParams.finding;
      $scope.userRole = userRole;
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
        functionsFtry4.verifyRoles($scope, projectName, userEmail, userRole);
        $scope.search();
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
      const projectName = $scope.project;
      const filterAux = $scope.filter;
      const filter = filterAux;
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

        // Handling presentation button
        const searchAt = $translate.instant("proj_alerts.search_title");
        const searchAc = $translate.instant("proj_alerts.search_cont");
        $msg.info(searchAc, searchAt);
        const reqProject = projectFtry.projectByName(projectName, filter);
        reqProject.then((response) => {
          $scope.view.project = true;
          if (!response.error) {
            if (angular.isUndefined(response.data)) {
              location.reload();
            }
            // Mixpanel tracking
            mixPanelDashboard.trackSearch(
              "SearchFinding",
              userEmail,
              projectName
            );
            $scope.data = response.data;
            projectData = response.data;
            const org = Organization.toUpperCase();
            const projt = $stateParams.project.toUpperCase();
            functionsFtry1.alertHeader(org, projt);
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
      return true;
    };
    $scope.urlIndicators = function urlIndicators () {
      $state.go("ProjectIndicators", {"project": $scope.project});
    };
    $scope.urlFindings = function urlFindings () {
      $state.go("ProjectFindings", {"project": $scope.project});
    };
    $scope.urlEvents = function urlEvents () {
      $state.go("ProjectEvents", {"project": $scope.project});
    };
    $scope.urlUsers = function urlUsers () {
      $state.go("ProjectUsers", {"project": $scope.project});
    };
    $scope.init();
  }
);
