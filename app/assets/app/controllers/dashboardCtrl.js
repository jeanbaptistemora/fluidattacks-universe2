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
    $uibModal
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

    $scope.initMyEventualities = function initMyEventualities () {
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
      const aux = $xhr.get($q, `${BASE.url}get_myevents`, {});
      aux.then((response) => {
        if (angular.isUndefined(response.data)) {
          location.reload();
        }
        else {
          for (let cont = 0; cont < response.data.length; cont++) {
            if (response.data[cont].type in keysToTranslate) {
              response.data[cont].type =
                  $translate.instant(keysToTranslate[response.data[cont].type]);
            }
            else {
              Rollbar.error(`Error: Couldn't find translation key for value: ${
                response.data[cont].type}`);
            }
          }
          angular.element("#myEventsTbl").bootstrapTable({
            "data": response.data,
            "locale": vlang,
            "onClickRow" (row) {
              $uibModal.open({
                "animation": true,
                "backdrop": "static",
                "controller" ($scope, data, $uibModalInstance) {
                  $scope.evnt = data;
                  // Tracking mixpanel
                  const org = Organization.toUpperCase();
                  const projt = $scope.evnt.fluidProject.toUpperCase();
                  mixPanelDashboard.trackReadEventuality(
                    userName,
                    userEmail,
                    org,
                    projt,
                    $scope.evnt.id
                  );
                  $scope.close = function close () {
                    $uibModalInstance.close();
                  };
                },
                "keyboard": false,
                "resolve": {"data": row},
                "templateUrl": "ver.html",
                "windowClass": "modal avance-modal"
              });
            }
          });
          angular.element("#myEventsTbl").bootstrapTable("refresh");
        }
      });
    };
    $scope.init = function init () {
      $scope.initMyProjects();
      $scope.initMyEventualities();
    };
    $scope.init();
  }
);
