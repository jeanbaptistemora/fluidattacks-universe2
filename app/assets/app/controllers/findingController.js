/**
 * @file findingController.js
 * @author engineering@fluid.la
 */
/**
 * Calcula la cardinalidad para el label resumen
 * @function calcCardinality
 * @param {Object} data
 * @return {undefined}
 */
integrates.calcCardinality = function(data){
    var cardinalidad = 0;
    data.data.forEach(function(i){
        cardinalidad += parseInt(i.cardinalidad);
    });
    $("#total_cardinalidad").html(cardinalidad);
    $("#total_hallazgos").html(data.data.length);
};
integrates.vuln_formatter = function(value, row, index){
    if (userRole == "analyst"){
        str = "<div class='btn-group'>"
            + "<a class='btn btn-default' href=':basedashboard#!/FindingResume/nid' target='_blank'><i class='glyphicon glyphicon-eye-open'></i></a>"
            + "<a class='btn btn-default' href=':basedashboard#!/vuln/update/?id=nid' target='_blank'><i class='glyphicon glyphicon-pencil'></i></a>"
            + "<a class='btn btn-default' href=':basedashboard#!/vuln/delete/?id=nid' target='_blank'><i class='glyphicon glyphicon-trash'></i></a></div>";
    }else{
        str = "<div class='btn-group'>"
            + "<a class='btn btn-default' href=':basedashboard#!/FindingResume/nid' target='_blank'><i class='glyphicon glyphicon-eye-open'></i></a>";
    }
    return str.replace(/nid/g, row.id).replace(/:base/g, BASE.url);
}
/**
 * Crea el controlador de la funcionalidad de vulnerabilidades
 * @name findingController
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {integrates.findingFactory} findingFactory
 * @return {undefined}
 */
integrates.controller("findingController", function($scope, $uibModal, $translate, $filter, findingFactory) {
    /**
     * Inicializa las variables del controlador de hallazgos
     * @function init
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.init = function(){
        $scope.userRole = userRole;
        $("#search_section").hide();
        $(".loader").hide();
        document.onkeypress = function(ev){ //asignar funcion a la tecla Enter
            if(ev.keyCode === 13){
                if($('#project').is(':focus')){
                    $scope.searchVulnByName();
                }
            }
        }
        $translate.use(localStorage['lang']);
    }
    /**
     * Despliega la modal de ver avance
     * @function openModalAvance
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.openModalAvance = function(){
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'avance.html',
            windowClass: 'modal avance-modal',
            controller: function($scope, $uibModalInstance){
                var data = $("#vulnerabilities").bootstrapTable('getData');
                for(i=0; i < data.length-1; i++){
                    for(j=i+1; j < data.length; j++){
                        if(parseFloat(data[i].criticidad) < parseFloat(data[j].criticidad)){
                            aux = data[i];
                            data[i] = data[j];
                            data[j] = aux;
                        }
                    }
                }
                $scope.rows = data;
                $scope.closeModalAvance = function(){
                    $uibModalInstance.dismiss('cancel');
                }
            },
            resolve: {
                ok: true
            }
        });
    };
    /**
     * Despliega la modal con las funciones de documentacion
     * @function openModalAutodoc
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.openModalAutodoc = function(){
        var project = $scope.project;
        var userRole = $scope.userRole;
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'autodoc_' + userRole + '.html',
            windowClass: 'modal avance-modal',
            controller: function($scope, $uibModalInstance, currentProject){
                $scope.project = currentProject;
                /**
                 * Descarga la documentacion automatica
                 * @function downloadDoc
                 * @param String kind
                 * @member integrates.findingController.openModalAutodoc
                 * @return {undefined}
                 */
                $scope.downloadDoc = function(kind){
                    var url = BASE.url + "export_autodoc?project=" + $scope.project;
                    url += "&format="+kind;
                    if(navigator.userAgent.indexOf("Firefox") == -1){
                        downLink = document.createElement("a");
                        downLink.target = "_blank";
                        downLink.href = url;
                        downLink.click();
                    }else{
                        win = window.open(url, '__blank');
                    }
                }
                /**
                 * Genera la documentacion automatica
                 * @function generateDoc
                 * @member integrates.findingController.openModalAutodoc
                 * @return {undefined}
                 */
                $scope.generateDoc = function(kind){
                    if (kind == ""
                        || kind == undefined) return false;
                    var data = $("#vulnerabilities").bootstrapTable('getData');
                    for(i=0; i < data.length-1; i++){
                        for(j=i+1; j < data.length; j++){
                            if(parseFloat(data[i].criticidad) < parseFloat(data[j].criticidad)){
                                aux = data[i];
                                data[i] = data[j];
                                data[j] = aux;
                            }
                        }
                    }
                    var project = $scope.project;
                    generateDoc = false;
                    try{
                        json = data;
                        generateDoc = true;
                        json = JSON.stringify(JSON.parse(JSON.stringify(json))); //remove indices
                        if (json == undefined) throw "error";
                        if (json == [] || json == {}) throw "error";
                        if(project.trim() == "") throw "error";
                    }catch(e){
                        generateDoc = false;
                    }
                    if(generateDoc){
                        findingFactory.generateDoc(project, json, kind).then(function(data){
                            var color = (data.error == false)?"success":"warning";
                            $.gritter.add({
                                title: '',
                                text: data.message,
                                class_name: 'color ' + color,
                                sticky: false,
                            });
                        }).catch(function(fallback) {
                            $.gritter.add({
                                title: 'Consultando',
                                text: 'Error...',
                                class_name: 'color warning',
                                sticky: false,
                            });
                        });
                    }else{
                        $.gritter.add({
                            title: 'Error',
                            text: 'Deben existir hallazgos y un nombre valido de proyecto',
                            class_name: 'color warning',
                            sticky: false,
                        });
                    }
                }
                /**
                 * Cierra la modal
                 * @function closeModal
                 * @member integrates.findingController.openModalAutodoc
                 * @return {undefined}
                 */
                $scope.closeModal = function(){
                    $uibModalInstance.dismiss('cancel');
                }
            },
            resolve: {
                currentProject: function(){
                    return $scope.project.toLowerCase();
                }
            }
        });
    };
    /**
     * Busca las vulnerabilidades por nombre de proyecto
     * @function searchVulnByName
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.searchVulnByName = function(){
        var project = $scope.project;
        var filter = $scope.filtro;
        if (project !== undefined
            && project !== ""){
            $scope.response = "";
            $.gritter.add({
                title: 'Consultando',
                text: 'Un momento porfavor...',
                class_name: 'color info',
                sticky: false,
            });
            $(".loader").show();
            findingFactory.getVulnByName(project, filter).then(function(data){
                if(data.error == false){
                    //Tracking Mixpanel
                    mixPanelDashboard.trackSearchFinding(userEmail, project);
                    //CONFIGURACION DE TABLA
                    $("#vulnerabilities").bootstrapTable('destroy');
                    $("#vulnerabilities").bootstrapTable(data);
                    $("#vulnerabilities").bootstrapTable('refresh');
                    //MANEJO DEL UI
                    $("#search_section").show();
                    $('[data-toggle="tooltip"]').tooltip();
                    integrates.calcCardinality(data);
                }else{
                    if (data.message == "Project doesn't exist"){
                        $.gritter.add({
                            title: 'Error',
                            text: 'El proyecto no existe...',
                            class_name: 'color warning',
                            sticky: false,
                        });
                    }else{
                        $.gritter.add({
                            title: 'Error',
                            text: e.message,
                            class_name: 'color warning',
                            sticky: false,
                        });
                        $scope.searchVulnByName();
                    }
                }
            }).catch(function(fallback) {
                $.gritter.add({
                    title: 'Consultando',
                    text: 'Error interno cargando datos...',
                    class_name: 'color warning',
                    sticky: false,
                });
                //$scope.searchVulnByName();
            });
        }else{
            $scope.response = "El nombre es obligatorio";
        }
    };
    /* Invoca la configuracion inicial del controlador */
    $scope.init();
});
