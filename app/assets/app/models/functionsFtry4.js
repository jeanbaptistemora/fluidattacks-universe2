/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global integrates, BASE, $xhr, $window, response:true, Organization, angular,
mixPanelDashboard,$msg, $, Rollbar, eventsData, releaseData:true,
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
  function functionsFtry1 (
    $document,
    $stateParams,
    $translate,
    $uibModal,
    $window,
    functionsFtry2,
    projectFtry2
  ) {
    return {

      "acceptRelease" ($scope) {
      // Get data
        const descData = {"id": $scope.finding.id};
        $uibModal.open({
          "animation": true,
          "backdrop": "static",
          "controller" (
            $scope,
            $uibModalInstance,
            updateData,
            $stateParams,
            $state
          ) {
            $scope.modalTitle = $translate.
              instant("confirmmodal.accept_release");
            $scope.ok = function ok () {
              // Make the request
              const req = projectFtry2.acceptRelease(updateData.id);
              // Capture the promise
              req.then((response) => {
                if (!response.error) {
                  if (response.message === "hasRelease") {
                    const errorAlert =
                                   $translate.instant("proj_alerts." +
                                    "releases_per_day");
                    $msg.error(errorAlert);
                    $uibModalInstance.close();
                    $state.go(
                      "ProjectReleases",
                      {"project": $stateParams.project}
                    );
                  }
                  else {
                    const updatedAt =
                                   $translate.instant("proj_alerts." +
                                    "updatedTitle");
                    const updatedAc =
                                   $translate.instant("proj_alerts." +
                                    "updated_cont");
                    $msg.success(updatedAc, updatedAt);
                    // Mixpanel tracking
                    mixPanelDashboard.trackFinding(
                      "acceptRelease",
                      userEmail,
                      descData.id
                    );
                    $uibModalInstance.close();
                    releaseData = [];
                    projectData = [];
                    $state.go(
                      "ProjectReleases",
                      {"project": $stateParams.project}
                    );
                  }
                }
                else if (response.error) {
                  const errorAc1 =
                                $translate.instant("proj_alerts.error_textsad");
                  Rollbar.error("Error: An error occurred accepting release");
                  $msg.error(errorAc1);
                }
              });
            };
            $scope.close = function close () {
              $uibModalInstance.close();
            };
          },
          "resolve": {"updateData": descData},
          "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
        });
      },
      "rejectRelease" ($scope) {
      // Get data
        const descData = {"id": $scope.finding.id};
        $uibModal.open({
          "animation": true,
          "backdrop": "static",
          "controller" (
            $scope,
            $uibModalInstance,
            updateData,
            $stateParams,
            $state
          ) {
            $scope.rejectData = {};
            $scope.modalTitle = $translate.
              instant("confirmmodal.reject_release");
            $scope.ok = function ok () {
              $scope.rejectData.id = updateData.id;
              // Make the request
              const req = projectFtry2.rejectRelease($scope.rejectData);
              // Capture the promise
              req.then((response) => {
                if (!response.error) {
                  const updatedAt =
                                 $translate.instant("proj_alerts.updatedTitle");
                  const updatedAc =
                                 $translate.instant("proj_alerts.updated_cont");
                  $msg.success(updatedAc, updatedAt);
                  // Mixpanel tracking
                  mixPanelDashboard.trackFinding(
                    "acceptRelease",
                    userEmail,
                    descData.id
                  );
                  $uibModalInstance.close();
                  releaseData = [];
                  projectData = [];
                  $state.go(
                    "ProjectReleases",
                    {"project": $stateParams.project}
                  );
                }
                else if (response.error) {
                  const errorAc1 =
                                $translate.instant("proj_alerts.error_textsad");
                  Rollbar.error("Error: An error occurred rejecting release");
                  $msg.error(errorAc1);
                }
              });
            };
            $scope.close = function close () {
              $uibModalInstance.close();
            };
          },
          "resolve": {"updateData": descData},
          "templateUrl": `${BASE.url}assets/views/project/rejectMdl.html`
        });
      }
    };
  }
);
