/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global integrates, BASE, $xhr, $window, response:true, Organization, angular,
mixPanelDashboard,$msg, $, Rollbar, eventsData, userEmail, userName,$document */
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "response"] }]*/
/**
 * @file functionsFtry1.js
 * @author engineering@fluidattacks.com
 */
/**
 * Factory definition for the 1st set of auxiliar functions.
 * @name functionsFtry1
 * @param {Object} $q Angular constructor
 * @param {Object} $translate Angular translator
 * @param {Object} projectFtry Factory with main functions
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "functionsFtry1",
  function functionsFtry1Function (
    $document,
    $stateParams,
    $translate,
    $uibModal,
    $window,
    functionsFtry2,
    projectFtry
  ) {
    return {

      "alertHeader" (company, project) {
        const req = projectFtry.getAlerts(company, project);
        req.then((response) => {
          if (!response.data) {
            location.reload();
          }
          else if (!response.errors) {
            const {alert} = response.data;
            if (alert.status === 1) {
              let html = "<div class=\"alert alert-danger-2\">";
              html += "<strong>Atención! </strong> :msg:</div>";
              html = html.replace(":msg:", alert.message);
              angular.element("#header_alert").html(html);
            }
          }
        });
      },

      "calculateFindingSeverity" (data) {
        let severity = 0;
        const MAX_SEVERITY = 5;
        const PERCENTAGE_FACTOR = 100.0;
        if (!isNaN(data.finding.severity)) {
          severity = parseFloat(data.finding.severity);
          if (severity < 0 || severity > MAX_SEVERITY) {
            Rollbar.error("Error: Severity must be an integer bewteen 0 and 5");
            $msg.error(
              $translate.instant("proj_alerts.error_severity"),
              "error"
            );
            data.finding.riskValue = "";
            return [
              false,
              data.finding.riskValue
            ];
          }
          try {
            let prob = data.finding.probability;
            severity = data.finding.severity;
            prob = prob.split("%")[0];
            prob = parseFloat(prob) / PERCENTAGE_FACTOR;
            severity = parseFloat(severity);
            const vRiesgo = prob * severity;
            const CRITIC_RISK = 3;
            const MODERATE_RISK = 2;
            if (vRiesgo >= CRITIC_RISK) {
              data.finding.riskValue = "(:r) Critico".replace(
                ":r",
                vRiesgo.toFixed(1)
              );
            }
            else if (vRiesgo >= MODERATE_RISK &&
                   vRiesgo < CRITIC_RISK) {
              data.finding.riskValue = "(:r) Moderado".replace(
                ":r",
                vRiesgo.toFixed(1)
              );
            }
            else {
              data.finding.riskValue = "(:r) Tolerable".replace(
                ":r",
                vRiesgo.toFixed(1)
              );
            }
            return [
              true,
              data.finding.riskValue
            ];
          }
          catch (err) {
            data.finding.riskValue = "";
            return [
              false,
              data.finding.riskValue
            ];
          }
        }
        else if (isNaN(data.finding.severity)) {
          Rollbar.error("Error: Severity must be an integer bewteen 0 and 5");
          $msg.error($translate.instant("proj_alerts.error_severity"), "error");
          data.finding.riskValue = "";
          return [
            false,
            data.finding.riskValue
          ];
        }
        return true;
      },

      "deleteFinding" ($scope) {
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
            $scope.vuln = {};
            $scope.modalTitle =
                               $translate.instant("confirmmodal.title_finding");
            $scope.ok = function ok () {
              // Make the request
              const req = projectFtry.deleteFinding(updateData.id, $scope.vuln);
              // Capture the promise
              req.then((response) => {
                if (!response.error) {
                  const updatedAt =
                                 $translate.instant("proj_alerts.updatedTitle");
                  const updatedAc =
                                 $translate.instant("proj_alerts.updated_cont");
                  $msg.success(updatedAc, updatedAt);
                  $uibModalInstance.close();
                  $state.go(
                    "ProjectFindings",
                    {"project": $stateParams.project}
                  );
                  // Mixpanel tracking
                  mixPanelDashboard.trackFinding(
                    "deleteFinding",
                    userEmail,
                    descData.id
                  );
                }
                else if (response.error) {
                  const errorAc1 =
                                $translate.instant("proj_alerts.error_textsad");
                  Rollbar.error("Error: An error occurred deleting finding");
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
          "templateUrl": `${BASE.url}assets/views/project/deleteMdl.html`
        });
      },

      "findingVerified" ($scope) {
        // Get data
        const currUrl = $window.location.href;
        const trackingUrl = currUrl.replace("/description", "/tracking");
        const descData = {
          "findingId": $scope.finding.id,
          "findingName": $scope.finding.finding,
          "findingUrl": trackingUrl,
          "findingVulns": $scope.finding.openVulnerabilities,
          "project": $scope.finding.projectName,
          "userMail": userEmail
        };
        $uibModal.open({
          "animation": true,
          "backdrop": "static",
          "controller" ($scope, $uibModalInstance, mailData) {
            $scope.modalTitle = $translate.instant("search_findings." +
                                          "tab_description.verified_finding");
            $scope.ok = function ok () {
              // Make the request
              const req =
                     projectFtry.findingVerified(mailData, mailData.findingId);
              // Capture the promise
              req.then((response) => {
                if (!response.error) {
                  // Mixpanel tracking
                  const org = Organization.toUpperCase();
                  const projt = descData.project.toUpperCase();
                  mixPanelDashboard.trackFindingDetailed(
                    "findingVerified",
                    userName,
                    userEmail,
                    org,
                    projt,
                    descData.findingId
                  );
                  const updatedAt = $translate.instant("proj_alerts." +
                                                     "updatedTitle");
                  const updatedAc = $translate.instant("proj_alerts." +
                                                   "verified_success");
                  $msg.success(updatedAc, updatedAt);
                  $uibModalInstance.close();
                  location.reload();
                }
                else if (response.error) {
                  Rollbar.error("Error: An error occurred " +
                            "when verifying the finding");
                  $msg.error($translate.instant("proj_alerts.error_textsad"));
                }
              });
            };
            $scope.close = function close () {
              $uibModalInstance.close();
            };
          },
          "keyboard": false,
          "resolve": {"mailData": descData},
          "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
        });
      },

      "treatmentEditable" ($scope) {
        functionsFtry2.goDown();
        if ($scope.onlyReadableTab4 === false) {
          $scope.finding.treatmentManager = userEmail;
          $scope.onlyReadableTab4 = true;
          $scope.finding.treatment = $scope.aux.treatment;
          $scope.finding.treatmentJustification = $scope.aux.razon;
          $scope.finding.btsExterno = $scope.aux.bts;
        }
        else if ($scope.onlyReadableTab4 === true) {
          $scope.finding.treatment = $scope.aux.treatment;
          $scope.finding.treatmentJustification = $scope.aux.razon;
          $scope.finding.treatmentManager = $scope.aux.responsable;
          $scope.finding.btsExterno = $scope.aux.bts;
          $scope.onlyReadableTab4 = false;
        }
      },

      "updateTreatment" ($scope) {
        const validateTreatment = function validateTreatment ($scope) {
          const minCharacter = 30;
          if ($scope.aux.razon === $scope.finding.treatmentJustification) {
            $msg.error($translate.instant("proj_alerts.differ_comment"));
            return false;
          }
          else if ($scope.finding.treatmentJustification === "") {
            $msg.error($translate.instant("proj_alerts.empty_comment"));
            return false;
          }
          else if ($scope.finding.treatmentJustification.length <
                   minCharacter) {
            $msg.error($translate.instant("proj_alerts.short_comment"));
            return false;
          }
          $scope.finding.treatmentManager = userEmail;
          return true;
        };
        let flag = false;
        if ($scope.aux.treatment === $scope.finding.treatment &&
        $scope.aux.razon === $scope.finding.treatmentJustification &&
        $scope.aux.bts !== $scope.finding.btsExterno) {
          flag = true;
        }
        else if (validateTreatment($scope)) {
          $scope.finding.treatmentManager = userEmail;
          flag = true;
        }
        if (flag === true) {
          const newData = {
            "externalBts": $scope.finding.btsExterno,
            "findingName": $scope.finding.finding,
            "id": $scope.finding.id,
            "projectName": $scope.finding.projectName,
            "treatment": $scope.finding.treatment,
            "treatmentJustification": $scope.finding.treatmentJustification,
            "treatmentManager": $scope.finding.treatmentManager
          };
          $uibModal.open({
            "animation": true,
            "backdrop": "static",
            "controller" ($scope, $uibModalInstance, updateData) {
              $scope.modalTitle = $translate.instant("search_findings." +
                                                 "tab_description." +
                                                 "update_treatmodal");
              $scope.ok = function ok () {
                // Make the request
                const req =
                        projectFtry.updateTreatment(updateData, updateData.id);
                // Capture the promise
                req.then((response) => {
                  if (!response.error) {
                    const org = Organization.toUpperCase();
                    const projt = $stateParams.project.toUpperCase();
                    mixPanelDashboard.trackFindingDetailed(
                      "FindingUpdateTreatment",
                      userName,
                      userEmail,
                      org,
                      projt,
                      newData.id
                    );
                    $msg.success(
                      $translate.instant("proj_alerts." +
                                           "updated_treat"),
                      $translate.instant("proj_alerts." +
                                                         "congratulation")
                    );
                    $uibModalInstance.close();
                    location.reload();
                  }
                  else if (response.error) {
                    Rollbar.error("Error: An error occurred " +
                                  "updating treatment");
                    const errorAc1 = $translate.instant("proj_alerts." +
                                                    "error_textsad");
                    $msg.error(errorAc1);
                  }
                });
              };

              $scope.close = function close () {
                $uibModalInstance.close();
              };
            },
            "keyboard": false,
            "resolve": {"updateData": newData},
            "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
          });
        }
      }
    };
  }
);
