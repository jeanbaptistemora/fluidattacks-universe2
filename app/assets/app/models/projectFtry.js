/* eslint no-magic-numbers: ["error", { "ignore": [500, 401] }]*/
/* global integrates, BASE, $xhr, location:true, $, Rollbar */
/**
 * @file projectFtry.js
 * @author engineering@fluidattacks.com
 */
/**
 * Crea el factory de la funcionalidad de hallazgos
 * @name projectFtry
 * @param {Object} $q
 * @return {undefined}
 */
integrates.factory("projectFtry", function ($q, $translate) {
  return {

    /**
     * Invoca el servicio para tener los hallazgos de un proyecto
     * @function projectByName
     * @param {String} project
     * @param {String} filter
     * @member integrates.projectFtry
     * @return {Object}
     */
    "projectByName" (project, filter) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.get($q, `${BASE.url}get_findings`, {
        project,
        filter,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para tener las eventualidades de un proyecto
     * @function EventualityByName
     * @param {String} project
     * @param {String} category
     * @member integrates.projectFtry
     * @return {Object}
     */
    "EventualityByName" (project, category) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.get($q, `${BASE.url}get_eventualities`, {
        project,
        category,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para tener el exploit de un hallazgo
     * @function getExploit
     * @param {String} link
     * @member integrates.projectFtry
     * @return {Object}
     */
    "getExploit" (findingid, id) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.get($q, `${BASE.url}get_exploit`, {
        findingid,
        id,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para tener el exploit de un hallazgo
     * @function getRecords
     * @param {String} findingid
     * @param {String} id
     * @member integrates.projectFtry
     * @return {Object}
     */
    "getRecords" (findingid, id) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.get($q, `${BASE.url}get_records`, {
        findingid,
        id,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para tener las evidencias de un hallazgo
     * @function getEvidences
     * @param {String} id
     * @member integrates.projectFtry
     * @return {Object}
     */
    "getEvidences" (id) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.get($q, `${BASE.url}get_evidences`, {
        id,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para tener los comentarios de un hallazgo
     * @function getComments
     * @param {String} id
     * @member integrates.projectFtry
     * @return {Object}
     */
    "getComments" (id) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.get($q, `${BASE.url}get_comments`, {
        id,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para agregar nuevos comentarios en un hallazgo
     * @function addComment
     * @param {String} id
     * @param {Object} data
     * @member integrates.projectFtry
     * @return {Object}
     */
    "addComment" (id, data) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.post($q, `${BASE.url}add_comment`, {
        id,
        data,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para eliminar los comentarios en un hallazgo
     * @function deleteComment
     * @param {String} id
     * @param {Object} data
     * @member integrates.projectFtry
     * @return {Object}
     */
    "deleteComment" (id, data) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.post($q, `${BASE.url}delete_comment`, {
        id,
        data,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para tener el detalle de un hallazgo
     * @function FindingById
     * @param {Integer} id
     * @member integrates.projectFtry
     * @return {Object}
     */
    "FindingById" (id) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.post($q, `${BASE.url}get_finding`, {
        id,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para tener el detalle de un hallazgo
     * @function ProjectDoc
     * @param {String} project
     * @param {JSON} json
     * @param {String} format
     * @member integrates.projectFtry
     * @return {Object}
     */
    "ProjectDoc" (project, json, format) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.post($q, `${BASE.url}generate_autodoc`, {
        project,
        "data": json,
        format,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para actualizar la seccion
     * cssv2 de un hallazgo
     * @function UpdateCSSv2
     * @param {JSON} data
     * @member integrates.projectFtry
     * @return {Object}
     */
    "UpdateCSSv2" (data) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.post($q, `${BASE.url}update_cssv2`, {
        data,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para actualizar la seccion
     * descriptiva de un hallazgo
     * @function UpdateDescription
     * @param {JSON} data
     * @member integrates.projectFtry
     * @return {Object}
     */
    "UpdateDescription" (data) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.post($q, `${BASE.url}update_description`, {
        data,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para actualizar el tratamiento de un hallazgo
     * @function UpdateTreatment
     * @param {JSON} data
     * @member integrates.projectFtry
     * @return {Object}
     */
    "UpdateTreatment" (data) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.post($q, `${BASE.url}update_treatment`, {
        data,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para actualizar la seccion
     * descriptiva de un hallazgo
     * @function DeleteFinding
     * @param {JSON} data
     * @member integrates.projectFtry
     * @return {Object}
     */
    "DeleteFinding" (data) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.post($q, `${BASE.url}delete_finding`, {
        data,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * @function FindingSolved
     * @param {JSON} data
     * @member integrates.projectFtry
     * @return {Object}s
     */
    "FindingSolved" (data) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.post($q, `${BASE.url}finding_solved`, {
        data,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para mostrar la severidad total del proyecto
     * @function RemediatedView
     * @param {String} project
     * @member integrates.projectFtry
     * @return {Object}s
     */
    "TotalSeverity" (project) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.get($q, `${BASE.url}total_severity`, {
        project,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para mostrar si fue remediado un hallazgo
     * @function RemediatedView
     * @param {JSON} data
     * @member integrates.projectFtry
     * @return {Object}s
     */
    "RemediatedView" (id) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.get($q, `${BASE.url}get_remediated`, {
        id,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para mostrar si fue verificado un hallazgo
     * @function FindingVerified
     * @param {JSON} data
     * @member integrates.projectFtry
     * @return {Object}s
     */
    "FindingVerified" (data) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.post($q, `${BASE.url}finding_verified`, {
        data,
        "_": Math.random()
      }, oops_ac);
    },
    "UpdateEvidenceFiles" (data, callbackFn, errorFn) {
      try {
        $.ajax({
          "url": `${BASE.url}update_evidences_files?_${Math.random()}`,
          "method": "POST",
          data,
          "mimeType": "multipart/form-data",
          "contentType": false,
          "cache": false,
          "processData": false,
          "success" (response) {
            $(".loader").hide();
            callbackFn(JSON.parse(response));
          },
          "error" (xhr, status, response) {
            $(".loader").hide();
            if (xhr.status == 500) {
              Rollbar.error("Error: An error ocurred loading data");
            }
            else if (xhr.status == 401) {
              Rollbar.error("Error: 401 Unauthorized");
              location = "error401";
            }
            errorFn(JSON.parse(response));
          }
        });
      }
      catch (e) {
        if (e.status == 401) {
          Rollbar.error("Error: 401 Unauthorized");
          location = "error401";
        }
        Rollbar.error("Error: An error ocurred getting finding by ID", e);
      }
    },
    "UpdateEvidenceText" (data) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.post($q, `${BASE.url}update_evidence_text`, {
        data,
        "_": Math.random()
      }, oops_ac);
    },

    /**
     * Invoca el servicio para tener las alertas de una compañia
     * @function getAlerts
     * @param {String} company
     * @param {String} project
     * @member integrates.projectFtry
     * @return {Object}
     */
    "getAlerts" (company, project) {
      const oops_ac = $translate.instant("proj_alerts.error_text");
      return $xhr.get($q, `${BASE.url}get_alerts`, {
        company,
        project,
        "_": Math.random()
      }, oops_ac);
    }
  };
});
