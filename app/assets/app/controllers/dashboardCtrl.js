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
    $timeout
  ) {
    $scope.initMyProjects = function initMyProjects () {
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
      $timeout(() => {
        angular.element("#myProjectsTbl").bootstrapTable({
          "locale": vlang,
          "onClickRow" (row) {
            $state.go("ProjectIndicators", {"project": row.project});
          },
          "url": `${BASE.url}get_myprojects`
        });
      });
    };

    $scope.init = function init () {
      $scope.initMyProjects();
    };
    $scope.init();
  }
);
