/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global integrates, BASE, $xhr, $window, response:true, Organization, angular,
mixPanelDashboard,$msg, $, Rollbar, eventsData, draftData:true,
projectData: true, userEmail, userName,$document */
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "response"] }]*/
/**
 * @file functionsFtry4.js
 * @author engineering@fluidattacks.com
 */
/**
 * Factory definition for the 1st set of auxiliar functions.
 * @name functionsFtry4
 * @param {Object} $q Angular constructor
 * @param {Object} $translate Angular translator
 * @param {Object} functionsFtry2 Factory with main functions
 * @param {Object} projectFtry2 Factory with main functions
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "functionsFtry4",
  function functionsFtry4 (
    $document,
    $stateParams,
    $timeout,
    $translate,
    $uibModal,
    $window,
    functionsFtry1,
    functionsFtry2,
    projectFtry,
    projectFtry2
  ) {
    return {
      "verifyRoles" ($scope, projectName, userEmail, userRole) {
        const customerAdmin =
                          projectFtry2.isCustomerAdmin(projectName, userEmail);
        customerAdmin.then((response) => {
          if (!response.error) {
            $scope.isProjectManager = response.data;
            $scope.isCustomer = userRole !== "customer" ||
                                $scope.isProjectManager;
          }
          else if (response.error) {
            $scope.isProjectManager = response.data;
            $scope.isCustomer = userRole !== "customer" ||
                                $scope.isProjectManager;
          }
        });
        $scope.isManager = userRole !== "customer" &&
                          userRole !== "customeradmin";
        $scope.isAdmin = userRole !== "customer" &&
                        userRole !== "customeradmin" && userRole !== "analyst";
      }
    };
  }
);
