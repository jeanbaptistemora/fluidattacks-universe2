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
              "search_findings.tab_description.action",
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
      "uploadVulnerabilites" ($scope) {
        const dataP = {};
        dataP.document = angular.element("#updatevulnerabilities").val();
        if (dataP.document === "") {
          const errorAc1 = $translate.instant("proj_alerts.error_textsad");
          $msg.error(errorAc1);
          return false;
        }
        const data = new FormData();
        const fileInput = angular.element("#updatevulnerabilities")[0];
        data.append("file", fileInput.files[0]);
        const fileName = fileInput.files[0].name;
        const dots = fileName.split(".");
        const fileType = `.${dots[dots.length - 1]}`;
        const validFileTypes = [
          ".yml",
          ".YML",
          ".yaml",
          ".YAML"
        ];
        const yamlMaxSize = 1048576;
        if (validFileTypes.indexOf(fileType) === -1) {
          const errorAc1 = $translate.instant("proj_alerts.file_type_yaml");
          $msg.error(errorAc1);
          return false;
        }
        if (fileInput.files[0].size > yamlMaxSize) {
          const errorAc1 = $translate.instant("proj_alerts.file_size_py");
          $msg.error(errorAc1);
          return false;
        }
        const responseFunction = function responseFunction (response) {
          if (response.errors) {
            let errorAc1 = "";
            for (let cont = 0; cont < response.errors.length; cont++) {
              if (response.errors[cont].message ===
                  "Exception - Error in range limit numbers") {
                errorAc1 = $translate.instant("proj_alerts.range_error");
              }
              else if (response.errors[cont].message ===
                  "Exception - Invalid Schema") {
                errorAc1 = $translate.instant("proj_alerts.invalid_schema");
              }
              else {
                errorAc1 = $translate.instant("proj_alerts.error_textsad");
              }
            }
            $msg.error(errorAc1);
          }
          else if (angular.isDefined(response.data.uploadFile) &&
              response.data.uploadFile.access) {
            if (response.data.uploadFile.success) {
              // Mixpanel tracking
              mixPanelDashboard.trackFinding(
                "UploadVulnerabilites",
                userEmail,
                $scope.finding.id
              );
              const updatedAt = $translate.instant("proj_alerts.updatedTitle");
              const updatedAc =
              $translate.instant("proj_alerts.updated_cont_file");
              $msg.success(updatedAc, updatedAt);
              location.reload();
            }
            else if (response.data.uploadFile.errorMessage === "invalid type") {
              const errorAc1 = $translate.instant("proj_alerts.file_type_yaml");
              $msg.error(errorAc1);
            }
            else if (response.data.uploadFile.errorMessage ===
              "file exceeds size limits") {
              const errorAc1 = $translate.instant("proj_alerts.file_size_py");
              $msg.error(errorAc1);
            }
            else {
              const errorAc1 = $translate.instant("proj_alerts.error_textsad");
              $msg.error(errorAc1);
            }
          }
          else {
            const errorAc1 = $translate.instant("proj_alerts.access_denied");
            $msg.error(errorAc1);
          }
        };
        projectFtry2.uploadVulnerabilities(
          data,
          $stateParams.id,
          responseFunction
        );
        return true;
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
