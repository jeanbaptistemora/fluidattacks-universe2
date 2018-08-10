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

      "acceptDraft" ($scope) {
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
              instant("confirmmodal.accept_draft");
            $scope.ok = function ok () {
              // Make the request
              const req = projectFtry2.acceptDraft(updateData.id);
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
                    "acceptDraft",
                    userEmail,
                    descData.id
                  );
                  $uibModalInstance.close();
                  draftData = [];
                  projectData = [];
                  $state.go(
                    "ProjectDrafts",
                    {"project": $stateParams.project}
                  );
                }
                else if (response.error) {
                  const errorAc1 =
                                $translate.instant("proj_alerts.error_textsad");
                  Rollbar.error("Error: An error occurred accepting draft");
                  $msg.error(errorAc1);
                }
              });
            };
            $scope.close = function close () {
              $uibModalInstance.close();
            };
          },
          "keyboard": false,
          "resolve": {"updateData": descData},
          "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
        });
      },
      "deleteDraft" ($scope) {
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
              instant("confirmmodal.delete_draft");
            $scope.ok = function ok () {
              // Make the request
              const req = projectFtry2.deleteDraft(updateData.id);
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
                    "deleteDraft",
                    userEmail,
                    descData.id
                  );
                  $uibModalInstance.close();
                  draftData = [];
                  projectData = [];
                  $state.go(
                    "ProjectDrafts",
                    {"project": $stateParams.project}
                  );
                }
                else if (response.error) {
                  const errorAc1 =
                                $translate.instant("proj_alerts.error_textsad");
                  Rollbar.error("Error: An error occurred rejecting draft");
                  $msg.error(errorAc1);
                }
              });
            };
            $scope.close = function close () {
              $uibModalInstance.close();
            };
          },
          "keyboard": false,
          "resolve": {"updateData": descData},
          "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
        });
      },
      "deleteProject" () {
      // Get data
        const descData = {"project": $stateParams.project};
        $uibModal.open({
          "animation": true,
          "backdrop": "static",
          "controller" (
            $scope,
            $uibModalInstance,
            data,
            $stateParams,
            $state
          ) {
            $scope.modalTitle =
                               $translate.instant("confirmmodal.title_project");
            $scope.ok = function ok () {
              // Make the request
              const req = projectFtry2.deleteProject(data.project);
              // Capture the promise
              req.then((response) => {
                if (!response.error) {
                  const updatedAt =
                                 $translate.instant("proj_alerts.updatedTitle");
                  const updatedAc =
                            $translate.instant("proj_alerts.project_deleted");
                  $msg.success(updatedAc, updatedAt);
                  $uibModalInstance.close();
                  $state.go("home");
                  // Mixpanel tracking
                  mixPanelDashboard.trackFinding(
                    "deleteProject",
                    userEmail,
                    descData.id
                  );
                }
                else if (response.error) {
                  const errorAc1 =
                                $translate.instant("proj_alerts.error_textsad");
                  Rollbar.error("Error: An error occurred deleting project");
                  $msg.error(errorAc1);
                }
              });
            };
            $scope.close = function close () {
              $uibModalInstance.close();
            };
          },
          "keyboard": false,
          "resolve": {"data": descData},
          "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
        });
      },
      "loadIndicatorsContent" ($scope, datatest) {
        const org = Organization.toUpperCase();
        const projt = $stateParams.project.toUpperCase();
        functionsFtry1.alertHeader(org, projt);
        $scope.calculateCardinality({"data": datatest});
        if (!$scope.isManager) {
          $scope.openEvents = projectFtry.alertEvents(eventsData);
          $scope.atAlert = $translate.instant("main_content.eventualities." +
                                              "descSingularAlert1");
          if ($scope.openEvents === 1) {
            $scope.descAlert1 = $translate.instant("main_content." +
                                            "eventualities.descSingularAlert2");
            $scope.descAlert2 = $translate.instant("main_content." +
                                            "eventualities.descSingularAlert3");
            angular.element("#events_alert").show();
          }
          else if ($scope.openEvents > 1) {
            $scope.descAlert1 = $translate.instant("main_content." +
                                              "eventualities.descPluralAlert1");
            $scope.descAlert2 = $translate.instant("main_content." +
                                              "eventualities.descPluralAlert2");
            angular.element("#events_alert").show();
          }
        }
        angular.element("#search_section").show();
        angular.element("[data-toggle=\"tooltip\"]").tooltip();

        if (angular.isDefined($stateParams.finding)) {
          $scope.finding.id = $stateParams.finding;
          $scope.view.project = false;
          $scope.view.finding = false;
        }
        $scope.data = datatest;
      },
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
