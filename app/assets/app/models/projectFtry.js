/* eslint no-magic-numbers: ["error", { "ignore": [500, 401] }]*/
/* global integrates, BASE, $xhr, window.location:true, $, Rollbar */
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
integrates.factory("projectFtry", ($q, $translate) => ({

  /**
   * Invoca el servicio para agregar nuevos comentarios en un hallazgo
   * @function addComment
   * @param {String} id Numeric id of the finding
   * @param {Object} data Data of the finding, including id of the comment
   * @member integrates.projectFtry
   * @return {Object} DynamoDB reponse about the post request
   */
  "addComment" (id, data) {
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.post($q, `${BASE.url}add_comment`, {
      "_": Math.random(),
      data,
      id
    }, oopsAc);
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.post($q, `${BASE.url}delete_comment`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.post($q, `${BASE.url}delete_finding`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.get($q, `${BASE.url}get_eventualities`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.post($q, `${BASE.url}get_finding`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.post($q, `${BASE.url}finding_solved`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.post($q, `${BASE.url}finding_verified`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.get($q, `${BASE.url}get_alerts`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.get($q, `${BASE.url}get_comments`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.get($q, `${BASE.url}get_evidences`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.get($q, `${BASE.url}get_exploit`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.get($q, `${BASE.url}get_records`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.get($q, `${BASE.url}get_findings`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.post($q, `${BASE.url}generate_autodoc`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.get($q, `${BASE.url}get_remediated`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.get($q, `${BASE.url}total_severity`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.post($q, `${BASE.url}update_cssv2`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.post($q, `${BASE.url}update_description`, {
      "_": Math.random(),
      data
    }, oopsAc);
  },

  "updateEvidenceFiles" (data, callbackFn, errorFn) {
    try {
      $.ajax({
        "cache": false,
        "contentType": false,
        data,
        "error" (xhr, status, response) {
          $(".loader").hide();
          if (xhr.status === 500) {
            Rollbar.error("Error: An error ocurred loading data");
          }
          else if (xhr.status === 401) {
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
        "url": `${BASE.url}update_evidences_files?_${Math.random()}`
      });
    }
    catch (err) {
      if (err.status === 401) {
        Rollbar.error("Error: 401 Unauthorized");
        window.location = "error401";
      }
      Rollbar.error("Error: An error ocurred getting finding by ID", err);
    }
  },

  "updateEvidenceText" (data) {
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.post($q, `${BASE.url}update_evidence_text`, {
      "_": Math.random(),
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
    const oopsAc = $translate.instant("proj_alerts.error_text");
    return $xhr.post($q, `${BASE.url}update_treatment`, {
      "_": Math.random(),
      data
    }, oopsAc);
  }
}));
