/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1,5]}]*/
/* global integrates, BASE, $xhr, window.location:true,
$, Rollbar, eventsData, secureRandom, angular */
/**
 * @file projectFtry.js
 * @author engineering@fluidattacks.com
 */
/**
 * Crea el factory de la funcionalidad de hallazgos
 * @name projectFtry
 * @param {Object} $q Angular constructor
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory("projectFtry", ($q) => ({

  /**
   * Invoca el servicio para agregar nuevos comentarios en un hallazgo
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
              parseFloat(data.impactoConfidencialidad.split(" | ")[0]);
    const ImpInt =
              parseFloat(data.impactoIntegridad.split(" | ")[0]);
    const ImpDis =
              parseFloat(data.impactoDisponibilidad.split(" | ")[0]);
    const AccCom = parseFloat(data.complejidadAcceso.split(" | ")[0]);
    const AccVec = parseFloat(data.vectorAcceso.split(" | ")[0]);
    const Auth = parseFloat(data.autenticacion.split(" | ")[0]);
    const Explo = parseFloat(data.explotabilidad.split(" | ")[0]);
    const Resol = parseFloat(data.nivelResolucion.split(" | ")[0]);
    const Confi = parseFloat(data.nivelConfianza.split(" | ")[0]);

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
    let cardinalidad = 0;
    let cardinalidadTotal = 0;
    let maximumSeverity = 0;
    let oldestFinding = 0;
    let openEvents = 0;
    data.data.forEach((cont) => {
      cardinalidad += parseInt(cont.cardinalidad, 10);
      cardinalidadTotal += parseInt(cont.cardinalidad_total, 10);
      if (maximumSeverity < cont.criticidad) {
        maximumSeverity = cont.criticidad;
      }
      if (oldestFinding < cont.edad) {
        oldestFinding = cont.edad;
      }
    });
    for (let event = 0; event < eventsData.length; event++) {
      if (eventsData[event].estado === "Unsolved" ||
            eventsData[event].estado === "Pendiente") {
        openEvents += 1;
      }
    }
    const metricColor = [
      "#2197d6;",
      "#aa2d30;",
      "#ff9930;",
      "#2e4050;",
      "#9f5ab1;",
      "#0a40ae;"
    ];
    const metricDes = [
      "findings",
      "cardinalities",
      "vulnerabilities",
      "maximumSeverity",
      "oldestFinding",
      "openEvents"
    ];
    const metricTool = [
      "findingsTooltip",
      "cardinalitiesTooltip",
      "vulnerabilitiesTooltip",
      "maximumSeverityTooltip",
      "oldestFindingTooltip",
      "openEventsTooltip"
    ];
    const metricIcon = [
      "s7-id",
      "s7-attention",
      "s7-info",
      "s7-gleam",
      "s7-date",
      "s7-way"
    ];
    const metricValue = [
      data.data.length,
      cardinalidad,
      cardinalidadTotal,
      maximumSeverity,
      oldestFinding,
      openEvents
    ];
    return [
      cardinalidad,
      cardinalidadTotal,
      metricColor,
      metricDes,
      metricIcon,
      metricTool,
      metricValue
    ];
  },

  /**
   * Invoca el servicio para eliminar los comentarios en un hallazgo
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
   * Invoca el servicio para actualizar la seccion
   * descriptiva de un hallazgo
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
   * Invoca el servicio para tener las eventualidades de un proyecto
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
   * Invoca el servicio para tener el detalle de un hallazgo
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
   * Invoca el servicio para mostrar si fue verificado un hallazgo
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
   * Invoca el servicio para tener las alertas de una compañia
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
   * Invoca el servicio para tener los comentarios de un hallazgo
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
   * Invoca el servicio para tener las evidencias de un hallazgo
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
   * Invoca el servicio para tener el exploit de un hallazgo
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
   * Invoca el servicio para tener los records de un hallazgo
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
   * Invoca el servicio para tener los hallazgos de un proyecto
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
   * Invoca el servicio para tener el detalle de un hallazgo
   * @function projectDoc
   * @param {String} project Project name
   * @param {JSON} json Data in project
   * @param {String} format Report type: Technical or Executive
   * @member integrates.projectFtry
   * @return {Object} Response about the report generation
   */
  "projectDoc" (project, json, format) {
    const oopsAc = "An error occurred generating documentation";
    return $xhr.post($q, `${BASE.url}generate_autodoc`, {
      "_": parseInt(secureRandom(5).join(""), 10),
      "data": json,
      format,
      project
    }, oopsAc);
  },

  /**
   * Invoca el servicio para mostrar si fue remediado un hallazgo
   * @function remediatedView
   * @param {String} id Numeric ID of a finding
   * @member integrates.projectFtry
   * @return {Object}  DynamoDB response about the remediate status of a finding
   */
  "remediatedView" (id) {
    const oopsAc = "An error occurred getting remediate state";
    return $xhr.get($q, `${BASE.url}get_remediated`, {
      "_": parseInt(secureRandom(5).join(""), 10),
      id
    }, oopsAc);
  },

  /**
   * Invoca el servicio para mostrar la severidad total del proyecto
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
   * Invoca el servicio para actualizar la seccion
   * cssv2 de un hallazgo
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
   * Invoca el servicio para actualizar la seccion
   * descriptiva de un hallazgo
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
          $(".loader").hide();
          if (xhr.status === INTERNAL_SERVER_ERROR) {
            Rollbar.error("Error: An error ocurred loading data");
          }
          else if (xhr.status === UNAUTHORIZED_ERROR) {
            Rollbar.error("Error: 401 Unauthorized");
            window.location = "error401";
          }
          errorFn(JSON.parse(response));
        },
        "method": "POST",
        "mimeType": "multipart/form-data",
        "processData": false,
        "success" (response) {
          $(".loader").hide();
          callbackFn(JSON.parse(response));
        },
        "url": `${BASE.url}update_evidences_files?_` +
                `${parseInt(secureRandom(5).join(""), 10)}`
      });
    }
    catch (err) {
      if (err.status === UNAUTHORIZED_ERROR) {
        Rollbar.error("Error: 401 Unauthorized");
        window.location = "error401";
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
   * Invoca el servicio para actualizar el tratamiento de un hallazgo
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
  }
}));
