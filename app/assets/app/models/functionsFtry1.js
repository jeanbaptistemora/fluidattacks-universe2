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
  function functionsFtry1 (
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
          if (angular.isUndefined(response.data)) {
            location.reload();
          }
          if (!response.error && response.data.length > 0) {
            if (response.data[0].status_act === "1") {
              let html = "<div class=\"alert alert-danger-2\">";
              html += "<strong>Atención! </strong>" +
                    `${response.data[0].message}</div>`;
              $document.getElementById("header_alert").innerHTML = html;
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
            let prob = data.finding.probabilidad;
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
              $scope.vuln.id = updateData.id;
              // Make the request
              const req = projectFtry.deleteFinding($scope.vuln);
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
          "findingName": $scope.finding.hallazgo,
          "findingUrl": trackingUrl,
          "findingVulns": $scope.finding.openVulnerabilities,
          "project": $scope.finding.fluid_project,
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
              const req = projectFtry.findingVerified(mailData);
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
          "resolve": {"mailData": descData},
          "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
        });
      },

      "treatmentEditable" ($scope) {
        functionsFtry2.goDown();
        if ($scope.onlyReadableTab4 === false) {
          $scope.finding.responsableTratamiento = userEmail;
          $scope.onlyReadableTab4 = true;
          $scope.finding.treatment = $scope.aux.treatment;
          $scope.finding.razonTratamiento = $scope.aux.razon;
          $scope.finding.btsExterno = $scope.aux.bts;
        }
        else if ($scope.onlyReadableTab4 === true) {
          $scope.finding.treatment = $scope.aux.treatment;
          $scope.finding.razonTratamiento = $scope.aux.razon;
          $scope.finding.responsableTratamiento = $scope.aux.responsable;
          $scope.finding.btsExterno = $scope.aux.bts;
          $scope.onlyReadableTab4 = false;
        }
      },

      "updateCSSv2" ($scope) {
      // Get the actual data in the severity fields
        const cssv2Data = {
          "accessComplexity": $scope.severityInfo.accessComplexity,
          "accessVector": $scope.severityInfo.accessVector,
          "authentication": $scope.severityInfo.authentication,
          "availabilityImpact": $scope.severityInfo.availabilityImpact,
          "confidenceLevel": $scope.severityInfo.confidenceLevel,
          "confidentialityImpact":
                                    $scope.severityInfo.confidentialityImpact,
          "exploitability": $scope.severityInfo.exploitability,
          "id": $scope.severityInfo.id,
          "integrityImpact": $scope.severityInfo.integrityImpact,
          "resolutionLevel": $scope.severityInfo.resolutionLevel
        };
        // Recalculate CSSV2
        functionsFtry2.findingCalculateCSSv2($scope);
        cssv2Data.criticity = $scope.finding.criticity;
        // Create an instance of the confirmation modal
        $uibModal.open({
          "animation": true,
          "backdrop": "static",
          "controller" ($scope, $uibModalInstance, updateData) {
            $scope.modalTitle = $translate.instant("confirmmodal.title_cssv2");
            $scope.ok = function ok () {
            // Make the request
              const req = projectFtry.updateCSSv2(updateData);
              // Capture the promise
              req.then((response) => {
                if (!response.error) {
                  const updatedAt = $translate.instant("proj_alerts." +
                                                     "updatedTitle");
                  const updatedAc = $translate.instant("proj_alerts." +
                                                     "updated_cont");
                  $msg.success(updatedAc, updatedAt);
                  $uibModalInstance.close();
                  location.reload();
                }
                else if (response.error) {
                  const errorAc1 = $translate.instant("proj_alerts." +
                                                   "error_textsad");
                  Rollbar.error("Error: An error occurred updating CSSv2");
                  $msg.error(errorAc1);
                }
              });
            };
            $scope.close = function close () {
              $uibModalInstance.close();
            };
          },
          "resolve": {"updateData": cssv2Data},
          "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
        });
      },

      "updateEvidenceText" (element, $scope) {
        const evImage = angular.element(element).attr("target");
        const data = {};
        data.id = $scope.finding.id;
        const description = angular.element(`#evidenceText${evImage}`).val();
        const file = angular.element(`#evidence${evImage}`).val();
        if (description === "" || $scope.evidenceDescription[evImage] ===
          description) {
          if (file !== "") {
            functionsFtry2.updateEvidencesFiles(element, $scope);
          }
          else if (file === "") {
            return false;
          }
        }
        else {
          if (evImage === "2") {
            data.descEvidencia1 = description;
            data.field = "descEvidencia1";
          }
          if (evImage === "3") {
            data.descEvidencia2 = description;
            data.field = "descEvidencia2";
          }
          if (evImage === "4") {
            data.descEvidencia3 = description;
            data.field = "descEvidencia3";
          }
          if (evImage === "5") {
            data.descEvidencia4 = description;
            data.field = "descEvidencia4";
          }
          if (evImage === "6") {
            data.descEvidencia5 = description;
            data.field = "descEvidencia5";
          }
          const req = projectFtry.updateEvidenceText(data);
          // Capture the promise
          req.then((response) => {
            if (!response.error) {
              const updatedAt = $translate.instant("proj_alerts.updatedTitle");
              const updatedAc = $translate.instant("proj_alerts." +
                                                 "updated_cont_description");
              $msg.success(updatedAc, updatedAt);
              if (file !== "") {
                functionsFtry2.updateEvidencesFiles(element, $scope);
              }
              else if (file === "") {
                location.reload();
              }
              return true;
            }
            const errorAc1 = $translate.instant("proj_alerts.no_text_update");
            Rollbar.error("Error: An error occurred updating " +
                        "evidences description");
            $msg.error(errorAc1);
            return false;
          });
        }
        return true;
      },

      "updateTreatment" ($scope) {
        const validateTreatment = function validateTreatment ($scope) {
          const minCharacter = 30;
          if ($scope.aux.razon === $scope.finding.razonTratamiento) {
            $msg.error($translate.instant("proj_alerts.differ_comment"));
            return false;
          }
          else if ($scope.finding.razonTratamiento === "") {
            $msg.error($translate.instant("proj_alerts.empty_comment"));
            return false;
          }
          else if ($scope.finding.razonTratamiento.length < minCharacter) {
            $msg.error($translate.instant("proj_alerts.short_comment"));
            return false;
          }
          $scope.finding.responsableTratamiento = userEmail;
          return true;
        };
        let flag = false;
        if ($scope.aux.treatment === $scope.finding.treatment &&
        $scope.aux.razon === $scope.finding.razonTratamiento &&
        $scope.aux.bts !== $scope.finding.btsExterno) {
          flag = true;
        }
        else if (validateTreatment($scope)) {
          $scope.finding.responsableTratamiento = userEmail;
          flag = true;
        }
        if (flag === true) {
          const newData = {
            "bts_externo": $scope.finding.btsExterno,
            "id": $scope.finding.id,
            "razonTratamiento": $scope.finding.razonTratamiento,
            "responsableTratamiento": $scope.finding.responsableTratamiento,
            "treatment": $scope.finding.treatment
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
                const req = projectFtry.updateTreatment(updateData);
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
            "resolve": {"updateData": newData},
            "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
          });
        }
      }
    };
  }
);
