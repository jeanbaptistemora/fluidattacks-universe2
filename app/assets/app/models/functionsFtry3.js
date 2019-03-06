/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1,3]}]*/
/* global integrates, BASE, $xhr, $window, response:true, Organization, angular,
mixPanelDashboard,$msg, $, Rollbar, eventsData, userEmail, userName, $document,
fieldsToTranslate, keysToTranslate, findingData, userRole, secureRandom */
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "response"] }]*/
/**
 * @file functionsFtry3.js
 * @author engineering@fluidattacks.com
 */
/**
 * Crea el factory de la funcionalidad de hallazgos
 * @name functionsFtry3
 * @param {Object} $q Angular constructor
 * @param {Object} $translate Angular translator
 * @param {Object} projectFtry Factory with main functions
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "functionsFtry3",
  function functionsFtry3Function (
    $document,
    $timeout,
    $translate,
    $uibModal,
    $window,
    functionsFtry1,
    functionsFtry2,
    functionsFtry4
  ) {
    return {
      "configKeyboardView" ($scope) {
        $document[0].onkeypress = function onkeypress (ev) {
          const enterKey = 13;
          if (ev.keyCode === enterKey) {
            if (angular.element("#project").is(":focus")) {
              $scope.search();
            }
          }
        };
      },

      "findingHeaderBuilding" ($scope, findingData) {
        $scope.header = {};
        $scope.header.findingTitle = $scope.finding.finding;
        findingData.header = $scope.header;
      }
    };
  }
);
