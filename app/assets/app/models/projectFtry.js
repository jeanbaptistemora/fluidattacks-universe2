/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1,5]}]*/
/* global integrates, BASE, $xhr, $window,
$, Rollbar, eventsData, secureRandom, angular */
/**
 * @file projectFtry.js
 * @author engineering@fluidattacks.com
 */
/**
 * Factory definition for some main set of functions.
 * @name projectFtry
 * @param {Object} $q Angular constructor
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "projectFtry",
  function projectFtryFunction ($q) {
    return {

      "alertEvents" (events) {
        let openEvents = 0;
        for (let event = 0; event < events.length; event++) {
          if (eventsData[event].eventStatus === "UNSOLVED") {
            openEvents += 1;
          }
        }
        return openEvents;
      },

      /**
       * Make a request to delete a finding
       * @function deleteFinding
       * @param {Integer} findingid Numeric ID of a finding
       * @param {JSON} data Data about the finding
       * @member integrates.projectFtry
       * @return {Object} Response with the status of the delete request
       */
      "deleteFinding" (findingid, data) {
        const oopsAc = "An error ocurred deleting finding";
        return $xhr.post($q, `${BASE.url}delete_finding`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data,
          findingid
        }, oopsAc);
      },

      /**
       * Return all the information for a specific findinf ID
       * @function findingById
       * @param {Integer} findingid Numeric ID of a finding
       * @param {String} project Project name
       * @member integrates.projectFtry
       * @return {Object} Formstack response with the data of a finding
       */
      "findingById" (findingid, project) {
        const oopsAc = "An error occurred getting finding";
        return $xhr.post($q, `${BASE.url}get_finding`, {
          findingid,
          project
        }, oopsAc);
      },

      /**
       * Return the alerts of a company.
       * @function getAlerts
       * @param {String} company Company name
       * @param {String} project Project name
       * @member integrates.projectFtry
       * @return {Object} Response by DynamoDB with project or company alerts
       */
      "getAlerts" (company, project) {
        const oopsAc = "An error occurred getting alerts";
        let gQry = `{
          alert(projectName:":prj", organization:":org"){
            message
            status
          }
        }`;
        gQry = gQry.replace(":prj", project.toLocaleLowerCase());
        gQry = gQry.replace(":org", company.toLocaleLowerCase());
        return $xhr.fetch($q, gQry, oopsAc);
      },

      /**
       * Return the eventualities of a project
       * @function getEvent
       * @param {String} eventId Event ID
       * @member integrates.projectFtry
       * @return {Object} Formstack response with the eventualities of a project
       */
      "getEvent" (eventId) {
        const oopsAc = "An error occurred getting event";
        const gQry = `{
             event (identifier: "${eventId}") {
               accessibility,
               affectation,
               affectedComponents,
               analyst,
               client,
               clientProject,
               eventDate,
               detail,
               evidence,
               id,
               projectName,
               eventStatus,
               eventType
             }
         }`;
        return $xhr.fetch($q, gQry, oopsAc);
      },

      /**
       * Make a request to get the all the findings in a project.
       * @function projectByName
       * @param {String} project Project name
       * @member integrates.projectFtry
       * @return {Object} Response by Formstack with findings data
       */
      "projectByName" (project) {
        const oopsAc = "An error occurred getting findings";
        return $xhr.get($q, `${BASE.url}get_findings`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          project
        }, oopsAc);
      },

      /**
       * Make a request to get the total severity of a project.
       * @function totalSeverity
       * @param {String} project Project name
       * @member integrates.projectFtry
       * @return {Object} DynamoDB response with the total severity of a project
       */
      "totalSeverity" (project) {
        const oopsAc = "An error occurred getting total severity";
        return $xhr.get($q, `${BASE.url}total_severity`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          project
        }, oopsAc);
      }
    };
  }
);
