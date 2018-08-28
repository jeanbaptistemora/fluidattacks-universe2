/* eslint no-shadow: ["error", { "allow": ["$scope"] }]*/
/* eslint no-magic-numbers: ["error", { "ignore":[-1,0,1] }]*/
/* global
integrates, $,   mixpanel, userMail, $xhr, Organization, userEmail, angular,
mixPanelDashboard, userName, projectData:true, eventsData:true, Rollbar, BASE,
findingData:true, fieldsToTranslate, keysToTranslate, modalInstance:true, $msg,
$window */
/**
 * @file dashboardController.js
 * @author engineering@fluidattacks.com
 */
/**
 * Controller definition for dashboard view.
 * @name dashboardController
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "dashboardCtrl",
  function dashboardCtrl (
    $q,
    $scope,
    $state,
    $stateParams,
    $timeout,
    $translate,
    dashboardFtry
  ) {
    $scope.goToProject = function goToProject (rowInfo) {
      $state.go("ProjectIndicators", {"project": rowInfo.project});
    };
    $scope.initMyProjects = function initMyProjects () {
      $scope.tblProjectHeaders = [
        {
          "Header": $translate.instant("main_content.projects.project_title"),
          "accessor": "project"
        },
        {
          "Header":
          $translate.instant("main_content.projects.project_description"),
          "accessor": "company_project"
        }
      ];
      dashboardFtry.getMyProjects().
        then((response) => {
          $scope.projectsDataset = response.data;
        });
    };

    $scope.init = function init () {
      $scope.initMyProjects();
    };
    $scope.init();
  }
);
