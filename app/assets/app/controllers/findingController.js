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
/**
 * Actualiza una fila de la tabla de hallazgos segun la respuesta de la modal
 * @function updateVulnRow
 * @param {Object} row 
 * @return {undefined}
 */
integrates.updateVulnRow = function(row){
    var data = $("#vulnerabilities").bootstrapTable("getData");
    for(var i=0; i<data.length;i++){
        if(data[i].id == row.id){
            data[i] = row
            $("#vulnerabilities").bootstrapTable("destroy");
            $("#vulnerabilities").bootstrapTable({data: data});
            $("#vulnerabilities").bootstrapTable("refresh");
            break;
        }
    }
    integrates.calcCardinality({data: data});
};
/**
 * Elimina una fila de la tabla de hallazgos segun la respuesta de la modal
 * @function deleteVulnRow
 * @param {Object} row 
 * @return {undefined}
 */
integrates.deleteVulnRow = function(row){
    var data = $("#vulnerabilities").bootstrapTable("getData")
    var newData = [];
    for(var i=0; i<data.length;i++){
        if(data[i].id != row.id){
            newData.append(row);
        }
    }
    $("#vulnerabilities").bootstrapTable("destroy");
    $("#vulnerabilities").bootstrapTable({data: newData});
    $("#vulnerabilities").bootstrapTable("refresh");
};
/**
 * Crea el controlador de la funcionalidad de vulnerabilidades
 * @name findingController 
 * @param {Object} $scope 
 * @param {Object} $uibModal
 * @param {integrates.findingFactory} findingFactory 
 * @return {undefined}
 */
integrates.controller("findingController", function($scope, $uibModal, findingFactory) {
    /**
     * Inicializa las variables del controlador de hallazgos
     * @function init
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.init = function(){
        $("#search_section").hide();
        $(".loader").hide();
        document.onkeypress = function(ev){ //asignar funcion a la tecla Enter
            if(ev.keyCode === 13){
                if($('#project').is(':focus')){
                    $scope.searchVulnByName();
                }        
            }
        }
    }
    /**
     * Despliega la modal de ver hallazgo
     * @function openModalVer
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.openModalVer = function(){
        var sel = $("#vulnerabilities").bootstrapTable('getSelections');
        if(sel.length == 0){
            $.gritter.add({
                title: 'Error',
                text: 'Debes seleccionar un hallazgo',
                class_name: 'color warning',
                    sticky: false,
            });
            return false;
        }else{
            $scope.currentVulnerability = sel[0];
        }
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'ver.html',
            windowClass: 'ver-modal',
            controller: function($scope, $uibModalInstance, currentVulnerability){
                $scope.vuln = currentVulnerability;
                if($scope.vuln.nivel == "General"){
                    $scope.esDetallado = "hide-detallado";
                    $scope.rows = "4";
                    $scope.cols = "12";
                }else{
                    $scope.esDetallado = "show-detallado";  
                    $scope.rows = "2";
                    $scope.cols = "6";
                }
                
                $scope.closeModalVer = function(){
                    $uibModalInstance.dismiss('cancel');
                }
            },
            resolve: {
                currentVulnerability: function(){
                    return $scope.currentVulnerability;
                }
            }
        });
    };
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
                $scope.rows = $("#vulnerabilities").bootstrapTable('getData');
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
     * Despliega la modal de ver editar hallazgo
     * @function openModalEditar
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.openModalEditar = function(){
        var sel = $("#vulnerabilities").bootstrapTable('getSelections');
        if(sel.length == 0){
            $.gritter.add({
                title: 'Error',
                text: 'Debes seleccionar un hallazgo',
                class_name: 'color warning',
                    sticky: false,
            });
            return false;
        }else{
            $scope.currentVulnerability = sel[0];
        }
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'editar.html',
            windowClass: 'ver-modal',
            controller: function($scope, $uibModalInstance, currentVulnerability){
                $scope.vuln = currentVulnerability;
                if($scope.vuln.nivel == "General"){
                    $scope.esDetallado = "hide-detallado";
                    $scope.rows = "4";
                    $scope.cols = "12";
                }else{
                    $scope.esDetallado = "show-detallado";  
                    $scope.rows = "2";
                    $scope.cols = "6";
                }
                $scope.okModalEditar = function(){
                   findingFactory.updateVuln($scope.vuln).then(function(response){
                        if(!response.error){
                            $.gritter.add({
                                title: 'Correcto!',
                                text: 'Hallazgo actualizado',
                                class_name: 'color success',
                                sticky: false,
                            });
                            integrates.updateVulnRow($scope.vuln);
                            $uibModalInstance.dismiss('cancel');
                        }else{
                            $.gritter.add({
                                title: 'Error!',
                                text: response.message,
                                class_name: 'color warning',
                                sticky: false,
                            });
                        } 
                   });
                }
                $scope.closeModalEditar = function(){
                    $uibModalInstance.dismiss('cancel');
                }
            },
            resolve: {
                currentVulnerability: function(){
                    return $scope.currentVulnerability;
                }
            }
        });
    };
    /**
     * Despliega la modal de ver eliminar hallazgo
     * @function openModalEliminar
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.openModalEliminar = function(){
        var sel = $("#vulnerabilities").bootstrapTable('getSelections');
        if(sel.length == 0){
            $.gritter.add({
                title: 'Error',
                text: 'Debes seleccionar un hallazgo',
                class_name: 'color warning',
                    sticky: false,
            });
            return false;
        }else{
            $scope.currentVulnerability = sel[0];
            $scope.currentVulnerability.justificacion = "";
        }
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'eliminar.html',
            windowClass: 'modal avance-modal',
            controller: function($scope, $uibModalInstance, currentVulnerability){
                $scope.vuln = currentVulnerability;
                $scope.closeModalEliminar = function(){
                    $uibModalInstance.dismiss('cancel');
                }
                $scope.okModalEliminar = function(){
                    if(typeof $scope.vuln.justificacion != "string"
                        || $scope.vuln.justificacion == ""){
                        $.gritter.add({
                            title: 'Error',
                            text: 'Debes seleccionar una justificacion',
                            class_name: 'color warning',
                            sticky: false,
                        });
                        return false;
                    }
                    findingFactory.deleteVuln($scope.vuln).then(function(response){
                        if(!response.error){
                            $.gritter.add({
                                title: 'Correcto!',
                                text: 'Hallazgo actualizado',
                                class_name: 'color success',
                                sticky: false,
                            });
                            integrates.deleteVulnRow($scope.vuln);
                            $uibModalInstance.dismiss('cancel');
                        }else{
                            $.gritter.add({
                                title: 'Error!',
                                text: response.message,
                                class_name: 'color warning',
                                sticky: false,
                            });
                        } 
                   });
                }
            },
            resolve: {
                currentVulnerability: function(){
                    return $scope.currentVulnerability;
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
        if (project !== undefined && project !== ""){
            $scope.response = "";
            $.gritter.add({
                title: 'Consultando',
                text: 'Un momento porfavor...',
                class_name: 'color info',
                    sticky: false,
            });
            $(".loader").show();
            findingFactory.getVulnByName(project).then(function(data){
                if(data.error == false){
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
                    text: 'Error de formstack...',
                    class_name: 'color warning',
                    sticky: false,
                });
                $scope.searchVulnByName();
            });
        }else{
            $scope.response = "El nombre es obligatorio";
        }
    };
    /**
     * Genera la documentacion automatica
     * @function generateDoc
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.generateDoc = function(){
        var json = $("#vulnerabilities").bootstrapTable("getData");
        var project = $scope.project;
        generateDoc = false;
        try{
            generateDoc = true;
            json = JSON.stringify(JSON.parse(JSON.stringify(json))); //remove indices
            if (json == undefined) throw "error";
            if (json == [] || json == {}) throw "error";
            if(project.trim() == "") throw "error";
        }catch(e){
            generateDoc = false;
        }
        if(generateDoc){
            findingFactory.generateDoc(project, json).then(function(data){
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
                    text: 'Error de formstack...',
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
    };
    /**
     * Descarga la documentacion automatica
     * @function downloadDoc
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.downloadDoc = function(){
        downLink = document.createElement("a");
        downLink.target = "_blank";
        downLink.href = "export_autodoc?project=" + $scope.project;
        downLink.click();
    };
    /* Invoca la configuracion inicial del controlador */
    $scope.init();
});


