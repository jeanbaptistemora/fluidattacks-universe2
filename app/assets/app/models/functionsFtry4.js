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
      "showVulnerabilities" ($scope, state) {
        const reqVulnerabilities =
          projectFtry2.getVulnerabilities($scope.finding.id, state);
        reqVulnerabilities.then((response) => {
          if (response.error) {
            if (angular.isUndefined(response.data.finding)) {
              $msg.error($translate.instant("proj_alerts.error_textsad"));
            }
          }
          else if (angular.isDefined(response.data.finding) &&
              response.data.finding.success) {
            const findingInfo = response.data.finding;
            const translationsStrings = [
              "search_findings.tab_description.ports",
              "search_findings.tab_description.port",
              "search_findings.tab_description.lines",
              "search_findings.tab_description.path",
              "search_findings.tab_description.line",
              "search_findings.tab_description.field",
              "search_findings.tab_description.inputs",
              "search_findings.tab_description.errorVuln",
              "proj_alerts.access_denied",
              "proj_alerts.error_textsad"
            ];
            $scope.vulnTranslations = {};
            angular.forEach(translationsStrings, (value) => {
              $scope.vulnTranslations[value] = $translate.instant(value);
            });
            if (findingInfo.portsVulns.length ||
                findingInfo.inputsVulns.length ||
                findingInfo.linesVulns.length) {
              angular.element(".has-vulnerabilities").show();
              angular.element(".has-old-vulnerabilities").hide();
            }
            else {
              angular.element(".has-old-vulnerabilities").show();
              angular.element(".has-vulnerabilities").hide();
            }
          }
          else if (response.data.finding.errorMessage === "Error in file") {
            const errorAc1 =
              $translate.instant("search_findings.tab_description.errorVuln");
            $msg.error(errorAc1);
          }
          else {
            $msg.error($translate.instant("proj_alerts.error_textsad"));
          }
        });
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
