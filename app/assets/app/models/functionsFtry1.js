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
      }
    };
  }
);
