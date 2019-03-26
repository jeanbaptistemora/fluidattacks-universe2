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
        let metricDes = [];
        let metricTool = [];
        let metricIcon = [];
        let metricValue = [];
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
        metricDes = [
          "findings",
          "vulnerabilities",
          "cardinalities",
          "maximumSeverity",
          "oldestFinding",
          "compromisedRecords"
        ];
        metricTool = [
          "findingsTooltip",
          "vulnerabilitiesTooltip",
          "cardinalitiesTooltip",
          "maximumSeverityTooltip",
          "oldestFindingTooltip",
          "compromisedRecordsTooltip"
        ];
        metricIcon = [
          "findings",
          "totalVulnerabilities",
          "openVulnerabilities",
          "vulnerabilities",
          "calendar",
          "total"
        ];
        metricValue = [
          data.data.length,
          cardinalidadTotal,
          openVulnerabilities,
          maximumSeverity,
          oldestFinding,
          compromisedRecords
        ];
        return [
          openVulnerabilities,
          cardinalidadTotal,
          metricDes,
          metricIcon,
          metricTool,
          metricValue
        ];
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
       * Return the events of a project
       * @function eventsByProject
       * @param {String} project Project name
       * @member integrates.projectFtry2
       * @return {Object} Database response with events info
       */
      "eventsByProject" (project) {
        const oopsAc = "An error occurred getting project events";
        const gQry = `{
            events (projectName: "${project}") {
              eventDate,
              detail,
              id,
              projectName,
              eventStatus,
              eventType
            }
        }`;
        return $xhr.fetch($q, gQry, oopsAc);
      },

      /**
       * Get project information.
       * @function getProject
       * @param {String} projectName Project Name
       * @member integrates.projectFtry2
       * @return {Object} GraphQL response with the requested data
       */
      "getProject" (projectName) {
        const oopsAc = "An error occurred getting project information";
        const gQry = `{
          project (projectName: "${projectName}") {
            name
            openVulnerabilities
            subscription
          }
        }`;
        return $xhr.fetch($q, gQry, oopsAc);
      },

      /**
       * Get user information.
       * @function getUserData
       * @param {String} email User email.
       * @param {String} project User project.
       * @member integrates.projectFtry2
       * @return {Object} GraphQL response with the requested data
       */
      "getUserData" (email, project) {
        const oopsAc = "An error occurred getting user information";
        const gQry = `{
          userData(projectName: "${project}", userEmail: "${email}") {
            organization
            responsability
            phoneNumber
          }
        }`;
        return $xhr.fetch($q, gQry, oopsAc);
      },

      /**
       * Get finding vulnerabilities.
       * @function getVulnerabilities
       * @param {String} findingId Numeric id of the finding
       * @member integrates.projectFtry2
       * @return {Object} GraphQL response with the requested data
       */
      "getVulnerabilities" (findingId) {
        const oopsAc = "An error occurred getting finding information";
        const gQry = `{
          finding(identifier: "${findingId}") {
            id
            success
            errorMessage
            openVulnerabilities
            closedVulnerabilities
          }
        }`;
        return $xhr.fetch($q, gQry, oopsAc);
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
      }
    };
  }
);
