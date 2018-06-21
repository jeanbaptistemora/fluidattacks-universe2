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
  function projectFtry (
    $q,
    $window
  ) {
    return {

      /**
       * Give access to an user in a project
       * @function addAccessIntegrates
       * @param {String} data Info of user to which access will be granted.
       * @member integrates.projectFtry
       * @return {Object} Response of request
       */
      "addAccessIntegrates" (data) {
        const oopsAc = "An error occurred getting events";
        return $xhr.post($q, `${BASE.url}add_access_integrates`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data
        }, oopsAc);
      },

      /**
       * Make a request to add new comment in a finding
       * @function addComment
       * @param {String} id Numeric id of the finding
       * @param {Object} data Data of the finding, including id of the comment
       * @member integrates.projectFtry
       * @return {Object} DynamoDB reponse about the post request
       */
      "addComment" (id, data) {
        const oopsAc = "An error occurred adding comment";
        return $xhr.post($q, `${BASE.url}add_comment`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data,
          id
        }, oopsAc);
      },
      "alertEvents" (events) {
        let openEvents = 0;
        for (let event = 0; event < events.length; event++) {
          if (eventsData[event].estado === "Unsolved" ||
            eventsData[event].estado === "Pendiente") {
            openEvents += 1;
          }
        }
        return openEvents;
      },
      "calCCssv2" (data) {
        const BASESCORE_FACTOR_1 = 0.6;
        const BASESCORE_FACTOR_2 = 0.4;
        const BASESCORE_FACTOR_3 = 1.5;
        const IMPACT_FACTOR = 10.41;
        const EXPLOITABILITY_FACTOR = 20;
        const F_IMPACT_FACTOR = 1.176;
        const ImpCon =
              parseFloat(data.confidentialityImpact.split(" | ")[0]);
        const ImpInt =
              parseFloat(data.integrityImpact.split(" | ")[0]);
        const ImpDis =
              parseFloat(data.availabilityImpact.split(" | ")[0]);
        const AccCom = parseFloat(data.accessComplexity.split(" | ")[0]);
        const AccVec = parseFloat(data.accessVector.split(" | ")[0]);
        const Auth = parseFloat(data.authentication.split(" | ")[0]);
        const Explo = parseFloat(data.exploitability.split(" | ")[0]);
        const Resol = parseFloat(data.resolutionLevel.split(" | ")[0]);
        const Confi = parseFloat(data.confidenceLevel.split(" | ")[0]);

        /*
         * The constants above are part of the BaseScore, Impact and
         * Exploibility equations
         * More information in https://www.first.org/cvss/v2/guide
         */
        const impact = IMPACT_FACTOR * (1 - ((1 - ImpCon) * (1 - ImpInt) *
                  (1 - ImpDis)));
        const exploitabilty = EXPLOITABILITY_FACTOR * AccCom * Auth * AccVec;
        const BaseScore = ((BASESCORE_FACTOR_1 * impact) + (BASESCORE_FACTOR_2 *
                        exploitabilty) - BASESCORE_FACTOR_3) * F_IMPACT_FACTOR;
        const Temporal = BaseScore * Explo * Resol * Confi;
        return [
          BaseScore,
          Temporal
        ];
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
        const showIndicator = ldclient.variation('integrates-indicator', false);
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
            "#0a40ae;",
            "#ff7373;"
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
        } else {
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
       * Make a request to delete a comment in a finding
       * @function deleteComment
       * @param {String} id Numeric id of the finding
       * @param {Object} data Data of the finding, including id of the comment
       * @member integrates.projectFtry
       * @return {Object} Response by DynamoDB about the delete request
       */
      "deleteComment" (id, data) {
        const oopsAc = "An error ocurred deleting comment";
        return $xhr.post($q, `${BASE.url}delete_comment`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data,
          id
        }, oopsAc);
      },

      /**
       * Make a request to delete a finding
       * @function deleteFinding
       * @param {JSON} data Data about the finding, including id
       * @member integrates.projectFtry
       * @return {Object} Response with the status of the delete request
       */
      "deleteFinding" (data) {
        const oopsAc = "An error ocurred deleting finding";
        return $xhr.post($q, `${BASE.url}delete_finding`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data
        }, oopsAc);
      },

      /**
       * Return the eventualities of a project
       * @function eventualityByName
       * @param {String} project Project name
       * @param {String} category Search filter: By Name or ID
       * @member integrates.projectFtry
       * @return {Object} Formstack response with the eventualities of a project
       */
      "eventualityByName" (project, category) {
        const oopsAc = "An error occurred getting events";
        return $xhr.get($q, `${BASE.url}get_eventualities`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          category,
          project
        }, oopsAc);
      },

      /**
       * Return all the information for a specific findinf ID
       * @function findingById
       * @param {Integer} id Numeric ID of a finding
       * @member integrates.projectFtry
       * @return {Object} Formstack response with the data of a finding
       */
      "findingById" (id) {
        const oopsAc = "An error occurred getting finding";
        return $xhr.post($q, `${BASE.url}get_finding`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          id
        }, oopsAc);
      },

      /**
       * @function findingSolved
       * @param {JSON} data Data about the finding, including id
       * @member integrates.projectFtry
       * @return {Object} Response about the verification request
       */
      "findingSolved" (data) {
        const oopsAc = "An error occurred when remediating the finding";
        return $xhr.post($q, `${BASE.url}finding_solved`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data
        }, oopsAc);
      },

      /**
       * Return a boolean saying whether the finding was verified or not.
       * @function findingVerified
       * @param {JSON} data Data about the finding, including id
       * @member integrates.projectFtry
       * @return {Object} Response about the verfication status of a finding
       */
      "findingVerified" (data) {
        const oopsAc = "An error occurred when verifying the finding";
        return $xhr.post($q, `${BASE.url}finding_verified`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data
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
        return $xhr.get($q, `${BASE.url}get_alerts`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          company,
          project
        }, oopsAc);
      },

      /**
       * Make a request to get the comments of a finding.
       * @function getComments
       * @param {String} id Numeric id of the finding
       * @member integrates.projectFtry
       * @return {Object} Response by DynamoDB finding comments
       */
      "getComments" (id) {
        const oopsAc = "An error ocurred getting comments";
        return $xhr.get($q, `${BASE.url}get_comments`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          id
        }, oopsAc);
      },

      /**
       * Make a request to get the evidences of a finding.
       * @function getEvidences
       * @param {String} id Numeric id of finding
       * @member integrates.projectFtry
       * @return {Object} Response by DynamoDB and S3 with finding evidences
       */
      "getEvidences" (id) {
        const oopsAc = "An error occurred getting evidences";
        return $xhr.get($q, `${BASE.url}get_evidences`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          id
        }, oopsAc);
      },

      /**
       * Make a request to get the exploit of a finding.
       * @function getExploit
       * @param {String} findingid Numeric id of finding
       * @param {String} id Unique id of the exploit
       * @member integrates.projectFtry
       * @return {Object} Response with exploit data
       */
      "getExploit" (findingid, id) {
        const oopsAc = "An error occurred getting exploit ID";
        return $xhr.get($q, `${BASE.url}get_exploit`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          findingid,
          id
        }, oopsAc);
      },

      /**
       * Make a request to get the records of a finding.
       * @function getRecords
       * @param {String} findingid Numeric id of finding
       * @param {String} id Unique id of the record
       * @member integrates.projectFtry
       * @return {Object} Response with records data
       */
      "getRecords" (findingid, id) {
        const oopsAc = "An error occurred getting records";
        return $xhr.get($q, `${BASE.url}get_records`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          findingid,
          id
        }, oopsAc);
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
       * Return a boolean saying whether the finding was remediated or not.
       * @function remediatedView
       * @param {String} id Numeric ID of a finding
       * @member integrates.projectFtry
       * @return {Object}  DynamoDB response about remediate status of a finding
       */
      "remediatedView" (id) {
        const oopsAc = "An error occurred getting remediate state";
        return $xhr.get($q, `${BASE.url}get_remediated`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          id
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
      },

      /**
       * Make a request to update the severity section of a finding.
       * @function updateCSSv2
       * @param {JSON} data New data in the severity tab
       * @member integrates.projectFtry
       * @return {Object} Formstack response about severity update request
       */
      "updateCSSv2" (data) {
        const oopsAc = "An error occurred updating CSSV2";
        return $xhr.post($q, `${BASE.url}update_cssv2`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data
        }, oopsAc);
      },

      /**
       * Make a request to update the description section of a finding.
       * @function updateDescription
       * @param {JSON} data New data in the description tab
       * @member integrates.projectFtry
       * @return {Object} Formstack response about description update request
       */
      "updateDescription" (data) {
        const oopsAc = "An error occurred updating description";
        return $xhr.post($q, `${BASE.url}update_description`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data
        }, oopsAc);
      },
      "updateEvidenceFiles" (data, callbackFn, errorFn) {
        const UNAUTHORIZED_ERROR = 401;
        const INTERNAL_SERVER_ERROR = 500;
        try {
          $.ajax({
            "cache": false,
            "contentType": false,
            data,
            "error" (xhr, status, response) {
              angular.element(".loader").hide();
              if (xhr.status === INTERNAL_SERVER_ERROR) {
                Rollbar.error("Error: An error ocurred loading data");
              }
              else if (xhr.status === UNAUTHORIZED_ERROR) {
                Rollbar.error("Error: 401 Unauthorized");
                $window.location = "error401";
              }
              errorFn(angular.fromJson(response));
            },
            "method": "POST",
            "mimeType": "multipart/form-data",
            "processData": false,
            "success" (response) {
              angular.element(".loader").hide();
              callbackFn(angular.fromJson(response));
            },
            "url": `${BASE.url}update_evidences_files?_` +
                `${parseInt(secureRandom(5).join(""), 10)}`
          });
        }
        catch (err) {
          if (err.status === UNAUTHORIZED_ERROR) {
            Rollbar.error("Error: 401 Unauthorized");
            $window.location = "error401";
          }
          Rollbar.error("Error: An error ocurred getting finding by ID", err);
        }
      },
      "updateEvidenceText" (data) {
        const oopsAc = "An error occurred updating evidence description";
        return $xhr.post($q, `${BASE.url}update_evidence_text`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data
        }, oopsAc);
      },

      /**
       * Make a request to update the treatment section of a finding.
       * @function updateTreatment
       * @param {JSON} data New data in the treatment section
       * @member integrates.projectFtry
       * @return {Object} Formstack response about the post request
       */
      "updateTreatment" (data) {
        const oopsAc = "An error occurred updating treatment";
        return $xhr.post($q, `${BASE.url}update_treatment`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          data
        }, oopsAc);
      },

      /**
       * Return the eventualities of a project
       * @function usersByProject
       * @param {String} project Project name
       * @member integrates.projectFtry
       * @return {Object} Formstack response with the eventualities of a project
       */
      "usersByProject" (project) {
        const oopsAc = "An error occurred getting events";
        return $xhr.get($q, `${BASE.url}get_users_login`, {
          "_": parseInt(secureRandom(5).join(""), 10),
          project
        }, oopsAc);
      }
    };
  }
);
