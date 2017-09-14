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
integrates.factory('projectFtry', function($q){
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
            return $xhr.get($q, BASE.url + "get_findings", {
                project: project, filter: filter, _: Math.random()
            });
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
            return $xhr.get($q, BASE.url + "get_eventualities", {
                project: project, category: category, _: Math.random()
            });
        },
        /**
         * Invoca el servicio para tener el detalle de un hallazgo
         * @function FindingById
         * @param {Integer} id
         * @member integrates.projectFtry
         * @return {Object}
         */
        FindingById: function(id){
            return $xhr.post($q, BASE.url + "get_finding", {
                id: id, _: Math.random()
            });
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
            return $xhr.post($q, BASE.url + "generate_autodoc", {
                project: project, data: json, format: format, _: Math.random()
            });
        }
    }
});