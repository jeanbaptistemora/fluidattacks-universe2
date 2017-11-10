/**
 * @file projectFtry.js
 * @author engineering@fluid.la
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
                data: json, _: Math.random()
            },oops_ac);
        }
    }
});
