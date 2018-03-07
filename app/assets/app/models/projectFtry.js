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
integrates.factory('projectFtry', function($q, $translate){
    return {
        /**
         * Invoca el servicio para tener los hallazgos de un proyecto
         * @function projectByName
         * @param {String} project
         * @param {String} filter
         * @member integrates.projectFtry
         * @return {Object}
         */
        projectByName: function(project, filter){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.get($q, BASE.url + "get_findings", {
                project: project, filter: filter, _: Math.random()
            },oops_ac);
        },
        /**
         * Invoca el servicio para tener las eventualidades de un proyecto
         * @function EventualityByName
         * @param {String} project
         * @param {String} category
         * @member integrates.projectFtry
         * @return {Object}
         */
        EventualityByName: function(project, category){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.get($q, BASE.url + "get_eventualities", {
                project: project, category: category, _: Math.random()
            },oops_ac);
        },
        /**
         * Invoca el servicio para tener el exploit de un hallazgo
         * @function getExploit
         * @param {String} link
         * @member integrates.projectFtry
         * @return {Object}
         */
        getExploit: function(findingid, id){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.get($q,  BASE.url + "get_exploit", {
                findingid: findingid, id: id, _: Math.random()
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
        getRecords: function(findingid, id){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.get($q,  BASE.url + "get_records", {
                findingid: findingid, id: id, _: Math.random()
            }, oops_ac);
        },
        /**
         * Invoca el servicio para tener las evidencias de un hallazgo
         * @function getEvidences
         * @param {String} id
         * @member integrates.projectFtry
         * @return {Object}
         */
        getEvidences: function(id){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.get($q, BASE.url + "get_evidences", {
                id: id, _: Math.random()
            },oops_ac)
        },
        /**
         * Invoca el servicio para tener los comentarios de un hallazgo
         * @function getComments
         * @param {String} id
         * @member integrates.projectFtry
         * @return {Object}
         */
        getComments: function(id){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.get($q, BASE.url + "get_comments", {
                id: id, _: Math.random()
            },oops_ac);
        },
        /**
         * Invoca el servicio para agregar nuevos comentarios en un hallazgo
         * @function addComment
         * @param {String} id
         * @param {Object} data
         * @member integrates.projectFtry
         * @return {Object}
         */
        addComment: function(id, data){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.post($q, BASE.url + "add_comment", {
                id: id, data: data, _: Math.random()
            },oops_ac);
        },
        /**
         * Invoca el servicio para eliminar los comentarios en un hallazgo
         * @function deleteComment
         * @param {String} id
         * @param {Object} data
         * @member integrates.projectFtry
         * @return {Object}
         */
        deleteComment: function(id, data){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.post($q, BASE.url + "delete_comment", {
                id: id, data: data, _: Math.random()
            },oops_ac);
        },
        /**
         * Invoca el servicio para tener el detalle de un hallazgo
         * @function FindingById
         * @param {Integer} id
         * @member integrates.projectFtry
         * @return {Object}
         */
        FindingById: function(id){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.post($q, BASE.url + "get_finding", {
                id: id, _: Math.random()
            },oops_ac);
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
        ProjectDoc: function(project, json, format){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.post($q, BASE.url + "generate_autodoc", {
                project: project, data: json, format: format, _: Math.random()
            },oops_ac);
        },
        /**
         * Invoca el servicio para actualizar la seccion
         * cssv2 de un hallazgo
         * @function UpdateCSSv2
         * @param {JSON} data
         * @member integrates.projectFtry
         * @return {Object}
         */
        UpdateCSSv2: function(data){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.post($q, BASE.url + "update_cssv2", {
                data, _: Math.random()
            },oops_ac);
        },
        /**
         * Invoca el servicio para actualizar la seccion
         * descriptiva de un hallazgo
         * @function UpdateDescription
         * @param {JSON} data
         * @member integrates.projectFtry
         * @return {Object}
         */
        UpdateDescription: function(data){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.post($q, BASE.url + "update_description", {
                data, _: Math.random()
            },oops_ac);
        },
        /**
         * Invoca el servicio para actualizar el tratamiento de un hallazgo
         * @function UpdateTreatment
         * @param {JSON} data
         * @member integrates.projectFtry
         * @return {Object}
         */
        UpdateTreatment: function(data){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.post($q, BASE.url + "update_treatment", {
                data, _: Math.random()
            },oops_ac);
        },
        /**
         * Invoca el servicio para actualizar la seccion
         * descriptiva de un hallazgo
         * @function DeleteFinding
         * @param {JSON} data
         * @member integrates.projectFtry
         * @return {Object}
         */
        DeleteFinding: function(data){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.post($q, BASE.url + "delete_finding", {
                data: data, _: Math.random()
            },oops_ac);
        },
        /**
         * @function FindingSolved
         * @param {JSON} data
         * @member integrates.projectFtry
         * @return {Object}s
         */
        FindingSolved: function(data){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.post($q, BASE.url + "finding_solved", {
                data, _: Math.random()
            },oops_ac);
        },
        /**
         * Invoca el servicio para mostrar la severidad total del proyecto
         * @function RemediatedView
         * @param {String} project
         * @member integrates.projectFtry
         * @return {Object}s
         */
        TotalSeverity: function(project){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.get($q, BASE.url + "total_severity", {
                project: project, _: Math.random()
            },oops_ac);
        },
        /**
         * Invoca el servicio para mostrar si fue remediado un hallazgo
         * @function RemediatedView
         * @param {JSON} data
         * @member integrates.projectFtry
         * @return {Object}s
         */
        RemediatedView: function(id){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.get($q, BASE.url + "get_remediated", {
                id: id, _: Math.random()
            },oops_ac);
        },
        /**
         * Invoca el servicio para mostrar si fue verificado un hallazgo
         * @function FindingVerified
         * @param {JSON} data
         * @member integrates.projectFtry
         * @return {Object}s
         */
        FindingVerified: function(data){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.post($q, BASE.url + "finding_verified", {
                data, _: Math.random()
            },oops_ac);
        },
        UpdateEvidenceFiles: function(data, callbackFn, errorFn){
            try {
                $.ajax({
                    url: BASE.url + "update_evidences_files?_"+ Math.random(),
                    method: "POST",
                    data: data,
                    mimeType: "multipart/form-data",
                    contentType: false,
                    cache: false,
                    processData: false,
                    success: function (response) {
                        $(".loader").hide();
                        callbackFn(JSON.parse(response));
                    },
                    error: function (xhr, status, response) {
                        $(".loader").hide();
                        if(xhr.status == 500){
                            Rollbar.error("Error: An error ocurred loading data");
                        }else if(xhr.status == 401){
                            Rollbar.error("Error: 401 Unauthorized");
                            location = "error401";
                        }
                        errorFn(JSON.parse(response));
                    }
                });
            } catch (e) {
                if(e.status == 401){
                    Rollbar.error("Error: 401 Unauthorized");
                    location = "error401";
                }
                Rollbar.error("Error: An error ocurred getting finding by ID", e);
            }
        },
        UpdateEvidenceText: function(data){
            var oops_ac = $translate.instant('proj_alerts.error_text');
            return $xhr.post($q, BASE.url + "update_evidence_text", {
                data, _: Math.random()
            },oops_ac);
        },
    }
});
