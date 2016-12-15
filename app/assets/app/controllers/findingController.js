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
    str = "<div class='btn-group'>" 
        + "<a class='btn btn-default' href='dashboard#/vuln/read/?id=nid' target='_blank'><i class='glyphicon glyphicon-eye-open'></i></a>"
        + "<a class='btn btn-default' href='dashboard#/vuln/update/?id=nid' target='_blank'><i class='glyphicon glyphicon-pencil'></i></a>"
        + "<a class='btn btn-default' href='dashboard#/vuln/delete/?id=nid' target='_blank'><i class='glyphicon glyphicon-trash'></i></a></div>";
    return str.replace(/nid/g,row.id);
}
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
     * Despliega la modal de vincular id y proyecto
     * @function openModalVincular
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.openModalVincular = function(){
        var project = $scope.project;
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'vincular.html',
            windowClass: 'modal avance-modal',
            controller: function($scope, $uibModalInstance, currentProject){
                $scope.project = currentProject;
                findingFactory.getIdByProject($scope.project).then(function(response){
                    if(!response.error){
                        $.gritter.add({
                            title: 'Correcto',
                            text: response.message,
                            class_name: 'color success',
                            sticky: false,
                        });
                        try{
                            $scope.order = parseInt(response.data);
                        }catch(e){
                            $scope.order = 0;
                            return false;
                        }
                    }else{
                        $.gritter.add({
                            title: 'Error',
                            text: response.message,
                            class_name: 'color warning',
                            sticky: false,
                        });
                        return false;
                    }
                });
                $scope.closeModal = function(){
                    $uibModalInstance.dismiss('cancel');
                }
                $scope.okModal = function(){
                    if($scope.order == 0 
                        || $scope.order.toString().length < 9
                        || typeof $scope.project != "string"
                        || $scope.project.trim() == ""){
                        $.gritter.add({
                            title: 'Error',
                            text: 'Debes escribir un ID y un proyecto',
                            class_name: 'color warning',
                            sticky: false,
                        });
                        return false;
                    }
                    findingFactory.updateOrderID($scope.order, $scope.project).then(function(response){
                        if(!response.error){
                            $.gritter.add({
                                title: 'Correcto',
                                text: response.message,
                                class_name: 'color success',
                                sticky: false,
                            });
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
                currentProject: function(){
                    return $scope.project.toUpperCase();
                }
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
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'autodoc.html',
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
                    var url = "export_autodoc?project=" + $scope.project;
                    url += "&format="+kind;
                    downLink = document.createElement("a");
                    downLink.target = "_blank";
                    downLink.href = url;
                    downLink.click();
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
    /* Invoca la configuracion inicial del controlador */
    $scope.init();
});


integrates.controller("findingUpdateController", function($scope, $uibModal, findingFactory, $stateParams) {
    $("#search_section").hide();
    var id = $stateParams.id;
    $scope.vuln = {};
    if(id !== undefined){
        id = id.replace(/[^0-9]+/g, "?");
        if(id.indexOf("?") > -1) window.close();
        $scope.id = id;
        findingFactory.getVulnById(id).then(function(response){
            if(!response.error){
                if(response.data == undefined) window.close();
                $.gritter.add({
                    title: 'Correcto!',
                    text: 'Hallazgo cargado',
                    class_name: 'color success',
                    sticky: false,
                });
                $("#search_section").fadeIn(200);
                var data = response.data;
                try{
                    data.cardinalidad = parseInt(data.cardinalidad);
                    data.criticidad = parseFloat(data.criticidad);
                }catch(e){
                    data.cardinalidad = 0;
                    data.criticidad = 0;
                }
                $scope.vuln = data;
                if($scope.vuln.nivel == "General"){
                    $scope.esDetallado = "hide-detallado";
                    $scope.esGeneral = "show-detallado";
                }else{
                    $scope.esDetallado = "show-detallado";  
                    $scope.esGeneral = "hide-detallado";  
                }
            }else{
                $.gritter.add({
                    title: 'Error!',
                    text: response.message,
                    class_name: 'color warning',
                    sticky: false,
                });
            } 
        });
    }else{
        window.close();
    }
    /**
     * Despliega la modal de ver editar hallazgo
     * @function openModalEditar
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.openModal = function(){
        
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'editar.html',
            windowClass: 'ver-modal',
            controller: function($scope, $uibModalInstance, currentVulnerability){
                $scope.okModal = function(){
                   $scope.vuln = currentVulnerability; 
                   findingFactory.updateVuln($scope.vuln).then(function(response){
                        if(!response.error){
                            $.gritter.add({
                                title: 'Correcto!',
                                text: 'Hallazgo actualizado',
                                class_name: 'color success',
                                sticky: false,
                            });
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
                $scope.closeModal = function(){
                    $uibModalInstance.dismiss('cancel');
                }
            },
            resolve: {
                currentVulnerability: function(){
                    return $scope.vuln;
                }
            }
        });
    };
});
integrates.controller("findingDeleteController", function($scope, $uibModal, findingFactory, $stateParams) {
    $("#search_section").hide();
    var id = $stateParams.id;
    $scope.vuln = {};
    if(id !== undefined){
        id = id.replace(/[^0-9]+/g, "?");
        if(id.indexOf("?") > -1) window.close();
        $scope.id = id;
        findingFactory.getVulnById(id).then(function(response){
            if(!response.error){
                if(response.data == undefined) window.close();
                $.gritter.add({
                    title: 'Correcto!',
                    text: 'Hallazgo cargado',
                    class_name: 'color success',
                    sticky: false,
                });
                $("#search_section").fadeIn(200);
                var data = response.data;
                $scope.vuln = data;
            }else{
                $.gritter.add({
                    title: 'Error!',
                    text: response.message,
                    class_name: 'color warning',
                    sticky: false,
                });
            } 
        });
    }else{
        window.close();
    }
    /**
     * Despliega la modal de ver eliminar hallazgo
     * @function openModal
     * @member integrates.findingDeleteController
     * @return {undefined}
     */
    $scope.openModal = function(){
        if(!$scope.vuln.justificacion){
            $.gritter.add({
                title: 'Error!',
                text: "Debes ingresar una justificacion!",
                class_name: 'color warning',
                sticky: false,
            });
            return false;
        }
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'eliminar.html',
            windowClass: 'modal',
            controller: function($scope, $uibModalInstance, currentVulnerability){
                $scope.okModal = function(){
                   $scope.vuln = currentVulnerability; 
                   findingFactory.deleteVuln($scope.vuln).then(function(response){
                        if(!response.error){
                            $.gritter.add({
                                title: 'Correcto!',
                                text: 'Hallazgo eliminado, la ventana se cerrara en 5 segundos',
                                class_name: 'color success',
                                sticky: false,
                            });
                            $uibModalInstance.dismiss('cancel');
                            setTimeout('window.close();',5000);
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
                $scope.closeModal = function(){
                    $uibModalInstance.dismiss('cancel');
                }
            },
            resolve: {
                currentVulnerability: function(){
                    return $scope.vuln;
                }
            }
        });
    };
});
integrates.controller("findingReadController", function($scope, findingFactory, $stateParams) {
    $("#search_section").hide();
    var id = $stateParams.id;
    $scope.vuln = {};
    if(id !== undefined){
        id = id.replace(/[^0-9]+/g, "");
        $scope.id = id;
        findingFactory.getVulnById(id).then(function(response){
            if(!response.error){
                if(response.data == undefined) window.close();
                $.gritter.add({
                    title: 'Correcto!',
                    text: 'Hallazgo cargado',
                    class_name: 'color success',
                    sticky: false,
                });
                $("#search_section").fadeIn(200);
                var data = response.data;
                $scope.vuln = data;
                if($scope.vuln.nivel == "General"){
                    $scope.esDetallado = "hide-detallado";
                    $scope.esGeneral = "show-detallado";
                }else{
                    $scope.esDetallado = "show-detallado";  
                    $scope.esGeneral = "hide-detallado";  
                }
            }else{
                $.gritter.add({
                    title: 'Error!',
                    text: response.message,
                    class_name: 'color warning',
                    sticky: false,
                });
            } 
        });
    }else{
        window.close();
    }
});