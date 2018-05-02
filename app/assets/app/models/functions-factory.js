/* eslint no-magic-numbers: ["error", { "ignore": [0,1,2,3,5,6,9,100.0,
                                                   500,1000,10000] }]*/
/* global integrates, BASE, $xhr, window.location:true, response:true,
Organization, mixPanelDashboard, mixPanelDashboard, mixPanelDashboard,$msg,
$, Rollbar, eventsData, userEmail, userName */
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "response"] }]*/
/**
 * @file functions-factory.js
 * @author engineering@fluidattacks.com
 */
/**
 * Crea el factory de la funcionalidad de hallazgos
 * @name functionsFtry
 * @param {Object} $q Angular constructor
 * @param {Object} $translate Angular translator
 * @param {Object} projectFtry Factory with main functions
 * @return {undefined}
 */
/** @export */
integrates.factory("functionsFtry", ($q, $translate, projectFtry) => ({

  "findingCalculateSeveridad" (data) {
    let severidad = 0;
    if (!isNaN(data.finding.severidad)) {
      severidad = parseFloat(data.finding.severidad);
      if (severidad < 0 || severidad > 5) {
        Rollbar.error("Error: Severity must be an integer bewteen 0 and 5");
        $msg.error($translate.instant("proj_alerts.error_severity"), "error");
        data.finding.valorRiesgo = "";
        return [
          false,
          data.finding.valorRiesgo
        ];
      }
      try {
        let prob = data.finding.probabilidad;
        severidad = data.finding.severidad;
        prob = prob.split("%")[0];
        prob = parseFloat(prob) / 100.0;
        severidad = parseFloat(severidad);
        const vRiesgo = prob * severidad;
        if (vRiesgo >= 3) {
          data.finding.valorRiesgo = "(:r) Critico".replace(
            ":r",
            vRiesgo.toFixed(1)
          );
        }
        else if (vRiesgo >= 2 && vRiesgo < 3) {
          data.finding.valorRiesgo = "(:r) Moderado".replace(
            ":r",
            vRiesgo.toFixed(1)
          );
        }
        else {
          data.finding.valorRiesgo = "(:r) Tolerable".replace(
            ":r",
            vRiesgo.toFixed(1)
          );
        }
        return [
          true,
          data.finding.valorRiesgo
        ];
      }
      catch (err) {
        data.finding.valorRiesgo = "";
        return [
          false,
          data.finding.valorRiesgo
        ];
      }
    }
    else if (isNaN(data.finding.severidad)) {
      Rollbar.error("Error: Severity must be an integer bewteen 0 and 5");
      $msg.error($translate.instant("proj_alerts.error_severity"), "error");
      data.finding.valorRiesgo = "";
      return [
        false,
        data.finding.valorRiesgo
      ];
    }
    return true;
  },

  "remediatedView" (data, userRole) {
    const isManager = userRole !== "customer";
    let isRemediated = true;
    if (typeof data.finding.id !== "undefined") {
      const req = projectFtry.remediatedView(data.finding.id);
      req.then((response) => {
        if (!response.error) {
          isRemediated = response.data.remediated;
          if (isManager && isRemediated) {
            $(".finding-verified").show();
          }
          else {
            $(".finding-verified").hide();
          }
        }
        else if (response.error) {
          Rollbar.error("Error: An error occurred when " +
                        "remediating/verifying the finding");
        }
      });
    }
    return [
      isRemediated,
      isManager
    ];
  }
}));
