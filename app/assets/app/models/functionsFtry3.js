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
        const cierresHallazgo = $scope.finding.cierres;
        const cierresTmp = [];
        for (let cont = 0; cont < cierresHallazgo.length; cont++) {
          const cierre = cierresHallazgo[cont];
          cierre.position = cont + 1;
          cierresTmp.push(cierre);
        }
        $scope.finding.cierres = cierresTmp;
        $scope.header.findingTitle = $scope.finding.finding;
        $scope.header.findingType = $scope.finding.testType;
        $scope.header.findingRisk = "";
        $scope.header.findingState = $scope.finding.estado;
        $scope.header.findingID = $scope.finding.id;
        $scope.header.findingValue = $scope.finding.criticity;
        const HIGH_CRITICITY = 7;
        const MODERATE_CRITICITY = 4;
        const findingValue = parseFloat($scope.finding.criticity);
        if (findingValue >= HIGH_CRITICITY) {
          $scope.header.findingValueDescription =
               $translate.instant("finding_formstack.criticity_header.high");
          $scope.header.findingValueColor = $scope.colors.critical;
        }
        else if (findingValue >= MODERATE_CRITICITY &&
               findingValue < HIGH_CRITICITY) {
          $scope.header.findingValueDescription =
            $translate.instant("finding_formstack.criticity_header.moderate");
          $scope.header.findingValueColor = $scope.colors.moderate;
        }
        else {
          $scope.header.findingValueDescription =
            $translate.instant("finding_formstack.criticity_header.tolerable");
          $scope.header.findingValueColor = $scope.colors.tolerable;
        }

        if ($scope.header.findingState === "Abierto" ||
          $scope.header.findingState === "Open") {
          $scope.header.findingStateColor = $scope.colors.critical;
        }
        else if ($scope.header.findingState === "Parcialmente cerrado" ||
               $scope.header.findingState === "Partially closed") {
          $scope.header.findingStateColor = $scope.colors.moderate;
        }
        else {
          $scope.header.findingStateColor = $scope.colors.ok;
        }
        $scope.header.releaseDate = "";
        if ("releaseDate" in $scope.finding) {
          $scope.header.releaseDate = $scope.finding.releaseDate.split(" ")[0];
        }
        $scope.header.findingCount = $scope.finding.openVulnerabilities;
        findingData.header = $scope.header;
      },

      "loadFindingContent" ($scope) {
        functionsFtry4.showVulnerabilities($scope);
      }
    };
  }
);
