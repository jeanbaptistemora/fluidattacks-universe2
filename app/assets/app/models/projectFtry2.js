/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1,5]}]*/
/* global integrates, BASE, $xhr, $window,
$, Rollbar, eventsData, secureRandom, angular, ldclient */
/**
 * @file projectFtry2.js
 * @author engineering@fluidattacks.com
 */
/**
 * Factory definition for some main set of functions.
 * @name projectFtry2
 * @param {Object} $q Angular constructor
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "projectFtry2",
  function projectFtry2Function ($q) {
    return {

      /**
       * Admin accept a draft.
       * @function acceptDraft
       * @param {String} findingid Finding id.
       * @member integrates.projectFtry2
       * @return {Object} Formstack response with updated data
       */
      "acceptDraft" (findingid) {
        const oopsAc = "An error occurred accepting draft";
        return $xhr.post($q, `${BASE.url}accept_draft`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          findingid
        }, oopsAc);
      },

      /**
       * Validate that a user has access to a project.
       * @function accessToProject
       * @param {String} project Project name.
       * @member integrates.projectFtry2
       * @return {Object} Formstack response with the releases of a project
       */
      "accessToProject" (project) {
        const oopsAc = "An error occurred getting releases";
        return $xhr.get($q, `${BASE.url}access_to_project`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          project
        }, oopsAc);
      },

      "calCardinality" (data) {
        let openVulnerabilities = 0;
        let cardinalidadTotal = 0;
        let maximumSeverity = 0;
        let oldestFinding = 0;
        let openEvents = 0;
        let metricColor = [];
        let metricDes = [];
        let metricTool = [];
        let metricIcon = [];
        let metricValue = [];
        const showIndicator = ldclient.variation("integrates-indicator", false);
        if (showIndicator) {
          let compromisedRecords = 0;
          angular.forEach(data.data, (cont) => {
            compromisedRecords += parseInt(cont.recordsNumber, 10);
            openVulnerabilities += parseInt(cont.openVulnerabilities, 10);
            cardinalidadTotal += parseInt(cont.cardinalidad_total, 10);
            if (maximumSeverity < parseFloat(cont.criticity)) {
              maximumSeverity = parseFloat(cont.criticity);
            }
            if (oldestFinding < parseInt(cont.edad, 10)) {
              oldestFinding = parseInt(cont.edad, 10);
            }
          });
          for (let event = 0; event < eventsData.length; event++) {
            if (eventsData[event].estado === "Unsolved" ||
              eventsData[event].estado === "Pendiente") {
              openEvents += 1;
            }
          }
          metricColor = [
            "#2197d6;",
            "#aa2d30;",
            "#ff9930;",
            "#2e4050;",
            "#9f5ab1;",
            "#ff3435;",
            "#0a40ae;"
          ];
          metricDes = [
            "findings",
            "cardinalities",
            "vulnerabilities",
            "maximumSeverity",
            "oldestFinding",
            "openEvents",
            "compromisedRecords"
          ];
          metricTool = [
            "findingsTooltip",
            "cardinalitiesTooltip",
            "vulnerabilitiesTooltip",
            "maximumSeverityTooltip",
            "oldestFindingTooltip",
            "openEventsTooltip",
            "compromisedRecordsTooltip"
          ];
          metricIcon = [
            "s7-id",
            "s7-attention",
            "s7-info",
            "s7-gleam",
            "s7-date",
            "s7-way",
            "s7-notebook"
          ];
          metricValue = [
            data.data.length,
            openVulnerabilities,
            cardinalidadTotal,
            maximumSeverity,
            oldestFinding,
            openEvents,
            compromisedRecords
          ];
        }
        else {
          angular.forEach(data.data, (cont) => {
            openVulnerabilities += parseInt(cont.openVulnerabilities, 10);
            cardinalidadTotal += parseInt(cont.cardinalidad_total, 10);
            if (maximumSeverity < parseFloat(cont.criticity)) {
              maximumSeverity = parseFloat(cont.criticity);
            }
            if (oldestFinding < parseInt(cont.edad, 10)) {
              oldestFinding = parseInt(cont.edad, 10);
            }
          });
          for (let event = 0; event < eventsData.length; event++) {
            if (eventsData[event].estado === "Unsolved" ||
              eventsData[event].estado === "Pendiente") {
              openEvents += 1;
            }
          }
          metricColor = [
            "#2197d6;",
            "#aa2d30;",
            "#ff9930;",
            "#2e4050;",
            "#9f5ab1;",
            "#0a40ae;"
          ];
          metricDes = [
            "findings",
            "cardinalities",
            "vulnerabilities",
            "maximumSeverity",
            "oldestFinding",
            "openEvents"
          ];
          metricTool = [
            "findingsTooltip",
            "cardinalitiesTooltip",
            "vulnerabilitiesTooltip",
            "maximumSeverityTooltip",
            "oldestFindingTooltip",
            "openEventsTooltip"
          ];
          metricIcon = [
            "s7-id",
            "s7-attention",
            "s7-info",
            "s7-gleam",
            "s7-date",
            "s7-way"
          ];
          metricValue = [
            data.data.length,
            openVulnerabilities,
            cardinalidadTotal,
            maximumSeverity,
            oldestFinding,
            openEvents
          ];
        }
        return [
          openVulnerabilities,
          cardinalidadTotal,
          metricColor,
          metricDes,
          metricIcon,
          metricTool,
          metricValue
        ];
      },

      /**
       * Admin delete a draft.
       * @function deleteDraft
       * @param {String} findingid Numeric id of the finding
       * @member integrates.projectFtry2
       * @return {Object} Formstack response with updated data
       */
      "deleteDraft" (findingid) {
        const oopsAc = "An error occurred deleting draft";
        return $xhr.post($q, `${BASE.url}delete_draft`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          findingid
        }, oopsAc);
      },

      /**
       * Get drafts by project name.
       * @function draftsByName
       * @param {String} project Project name.
       * @member integrates.projectFtry2
       * @return {Object} Formstack response with the drafts of a project
       */
      "draftsByName" (project) {
        const oopsAc = "An error occurred getting drafts";
        return $xhr.get($q, `${BASE.url}get_drafts`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          project
        }, oopsAc);
      },

      /**
       * Set the customer admin  of a project.
       * @function changeUserRole
       * @param {String} data New user data.
       * @param {String} project New user project.
       * @member integrates.projectFtry2
       * @return {Object} Response by SQL DB
       */
      "editUser" (data, project) {
        const oopsAc = "An error occurred setting project admin";
        return $xhr.post($q, `${BASE.url}edit_user`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data,
          project
        }, oopsAc);
      },

      /**
       * Get role of a user.
       * @function isCustomerAdmin
       * @param {String} project Project name.
       * @param {String} email User email.
       * @member integrates.projectFtry2
       * @return {Object} Formstack response with the releases of a project
       */
      "isCustomerAdmin" (project, email) {
        const oopsAc = "An error occurred getting user role";
        return $xhr.get($q, `${BASE.url}is_customer_admin`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          email,
          project
        }, oopsAc);
      },

      /**
       * Give access to an user in a project
       * @function removeAccessIntegrates
       * @param {String} email Email of user to which access will be removed.
       * @param {String} project Project name.
       * @member integrates.projectFtry
       * @return {Object} Response of request
       */
      "removeAccessIntegrates" (email, project) {
        const oopsAc = "An error occurred removing access to an user";
        return $xhr.post($q, `${BASE.url}remove_access_integrates`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          email,
          project
        }, oopsAc);
      }
    };
  }
);
