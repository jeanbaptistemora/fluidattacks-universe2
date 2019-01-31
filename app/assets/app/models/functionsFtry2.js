/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global integrates, BASE, $xhr, response:true, Organization, $msg, $window,
$, Rollbar, eventsData, userEmail, userName, findingType, categories,
probabilities, actor, scenario, accessVector, accessComplexity, authentication,
confidenciality, integrity, availability, explotability, resolutionLevel,
realiabilityLevel, functionsFtry1, angular, mixPanelDashboard */
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "response"] }]*/
/**
 * @file functionsFtry2.js
 * @author engineering@fluidattacks.com
 */
/**
 * Factory definition for the 2nd set of auxiliar functions.
 * @name functionsFtry2
 * @param {Object} $q Angular constructor
 * @param {Object} $translate Angular translator
 * @param {Object} projectFtry Factory with main functions
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "functionsFtry2",
  function functionsFtry2Function (
    $injector,
    $stateParams,
    $translate,
    $window
  ) {
    return {

      "activeTab" (tabName, errorName, org, projt, id) {
        const tabNames = {
          "#comment": "#commentItem",
          "#cssv2": "#cssv2Item",
          "#evidence": "#evidenceItem",
          "#exploit": "#exploitItem",
          "#info": "#infoItem",
          "#observations": "#observationsItem",
          "#records": "#recordsItem",
          "#tracking": "#trackingItem"
        };
        for (let inc = 0; inc < Object.keys(tabNames).length; inc++) {
          if (Object.keys(tabNames)[inc] === tabName) {
            angular.element(tabName).addClass("active");
            angular.element(tabNames[tabName]).addClass("active");
          }
          else {
            angular.element(Object.keys(tabNames)[inc]).removeClass("active");
            angular.element(tabNames[
              Object.keys(tabNames)[inc]]).removeClass("active");
          }
        }
        // Mixpanel tracking
        mixPanelDashboard.trackFindingDetailed(
          errorName,
          userName,
          userEmail,
          org,
          projt,
          id
        );
      },

      "goDown" () {
      // eslint-disable-next-line angular/document-service
        $window.scrollTo(0, document.body.scrollHeight);
      }
    };
  }
);
