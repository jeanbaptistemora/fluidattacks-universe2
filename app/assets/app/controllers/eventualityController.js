/**
 * @file eventualityController.js
 * @author engineering@fluidattacks.com
 */
/**
 * Cambia el formato de una de las columnas de la tabla de eventualidades
 * @function afectacionFormatter
 * @param {String} value
 * @param {Object} row
 * @param {Number} index
 * @return {String}
 */
integrates.afectacionFormatter = function(value, row, index){
    if(value === undefined)
        {return "0";} //fix
    if(!isFinite(value))
        {if (value.trim() == "")
            {return "0";}}
    return value;
};
/**
 * Calcula la afectacion total para el label resumen
 * @function evntTotalize
 * @param {Object} data
 * @return {undefined}
 */
integrates.evntTotalize = function(data){
    var cardinalidad = 0;
    var afectacion = 0;
    for(var i = 0; i< data.data.length;i++){
        auxAfectacion = 0;
        if (data.data[i].afectacion != ""){
            auxAfectacion += parseInt(data.data[i].afectacion);
        }
        afectacion+=auxAfectacion;
    }
    $("#total_eventualidades").html(data.data.length);
    $("#total_afectacion").html(afectacion);
};
/**
 * Actualiza una fila de la tabla
 * @function updateEvntRow
 * @param {Object} data
 * @return {undefined}
 */
integrates.updateEvntRow = function(row){
    var data = $("#eventualities").bootstrapTable("getData");
    var newData = [];
    for(var i=0; i< data.length;i++){
        delete data[i][i.toString()];
        if(data[i].id == row.id){
            newData.push(row);
        }else{
            newData.push(data[i]);
        }
    }
    $("#eventualities").bootstrapTable("destroy");
    $("#eventualities").bootstrapTable({data: newData});
     $("#eventualities").bootstrapTable("refresh");
    integrates.evntTotalize({data: data});
};
/**
 * Crea el controlador de la funcionalidad de eventualidades
 * @name eventualityController
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {integrates.eventualityFactory} eventualityFactory
 * @return {undefined}
 */
integrates.controller("eventualityController", function($scope, $uibModal, $translate, eventualityFactory) {
     var attent_title = $translate.instant('proj_alerts.attent_title');
     var updated_title = $translate.instant('proj_alerts.updated_title');
     var event_title = $translate.instant('proj_alerts.event_title');
     var event_wait = $translate.instant('proj_alerts.event_wait');
     var event_select = $translate.instant('proj_alerts.event_select');
     var event_required = $translate.instant('proj_alerts.event_required');
     var event_internal = $translate.instant('proj_alerts.event_internal');
     var event_formstack = $translate.instant('proj_alerts.event_formstack');
     var event_positiveint = $translate.instant('proj_alerts.event_positiveint');
     var event_updated = $translate.instant('proj_alerts.event_updated');
     var event_exist = $translate.instant('proj_alerts.event_exist');
     /**
     * Inicializa las variables del controlador de eventualidades
     * @function init
     * @member integrates.eventualityController
     * @return {undefined}
     */
    $scope.init = function(){
        $("#search_section").hide();
        $(".loader").hide();
        document.onkeypress = function(ev){ //asignar funcion a la tecla Enter
            if(ev.keyCode === 13){
                if($('#project').is(':focus')){
                    $scope.searchEvntByName();
                }
            }
        }
        mixpanel.track(
        "SearchEventuality", {
            "Email": userEmail,
            }
        );
        $scope.view = {};
        $scope.view.event = false;
    }
    /**
     * Despliega la modal de ver eventualidad
     * @function openModalVer
     * @member integrates.eventualityController
     * @return {undefined}
     */
    $scope.openModalVer = function(){
        var sel = $("#eventualities").bootstrapTable('getSelections');
        if(sel.length == 0){
            Rollbar.error("Error: No events are selected");
            $.gritter.add({
                title: 'Error',
                text: event_select,
                class_name: 'color warning',
                    sticky: false,
            });
            return false;
        }
            $scope.currentEventuality = sel[0];
        
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'ver.html',
            windowClass: 'ver-modal',
            controller: function($scope, $uibModalInstance, currentEventuality){
                if (currentEventuality.afectacion == ""){
                    currentEventuality.afectacion = "0";
                }
                $scope.evnt = currentEventuality;
                $scope.evnt.afectacion = parseInt(currentEventuality.afectacion);
                $scope.closeModalVer = function(){
                    $uibModalInstance.close();
                }
            },
            resolve: {
                currentEventuality: function(){
                    return $scope.currentEventuality;
                }
            }
        });
    };
    /**
     * Despliega la modal de ver resumen de eventualidades
     * @function openModalAvance
     * @member integrates.eventualityController
     * @return {undefined}
     */
    $scope.openModalAvance = function(){
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'avance.html',
            windowClass: 'modal avance-modal',
            controller: function($scope, $uibModalInstance){
                $scope.rows = $("#eventualities").bootstrapTable('getData');
                $scope.closeModalAvance = function(){
                    $uibModalInstance.close();
                }
            },
            resolve: {
                ok: true
            }
        });
    };
    /**
     * Despliega la modal de editar eventualidades
     * @function openModalEditar
     * @member integrates.eventualityController
     * @return {undefined}
     */
    $scope.openModalEditar = function(){
        var sel = $("#eventualities").bootstrapTable('getSelections');
        if(sel.length == 0){
            Rollbar.error("Error: No events are selected");
            $.gritter.add({
                title: 'Error',
                text: event_select,
                class_name: 'color warning',
                sticky: false,
            });
            return false;
        }
            $scope.currentEventuality = sel[0];
        

        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'editar.html',
            windowClass: 'ver-modal',
            controller: function($scope, $uibModalInstance, currentEventuality){
                if (currentEventuality.afectacion == ""){
                    currentEventuality.afectacion = "0";
                }
                $scope.evnt = currentEventuality;
                $scope.evnt.afectacion = parseInt(currentEventuality.afectacion);

                $scope.okModalEditar = function(){
                   submit = false;
                   try{
                       if($scope.evnt.afectacion == undefined){
                           throw "negativo";
                       }
                       submit = true;
                   }catch(e){
                        Rollbar.error("Error: Affectation can not be a negative number");
                       $.gritter.add({
                            title: attent_title,
                            text: event_positiveint,
                            class_name: 'color warning',
                            sticky: false,
                       });
                       return false;
                   }
                   eventualityFactory.updateEvnt($scope.evnt).then(function(response){
                        if(!response.error){
                            $.gritter.add({
                                title: updated_title,
                                text: event_updated,
                                class_name: 'color success',
                                sticky: false,
                            });
                            integrates.updateEvntRow($scope.evnt);
                            $uibModalInstance.close();
                        }else{
                            Rollbar.error("Error: An error occurred updating events");
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
                    $uibModalInstance.close();
                }
            },
            resolve: {
                currentEventuality: function(){
                    return $scope.currentEventuality;
                }
            }
        });
    };
    $scope.category = "Name";
    $scope.setCategory = function(category){
        $scope.category = category;
    }
    /**
     * Busca las eventualidades por nombre de proyecto
     * @function searchEvntByName
     * @member integrates.eventualityController
     * @return {undefined}
     */
    $scope.searchEvntByName = function(){
        var vlang;
        if(localStorage.lang === "en"){
          vlang = 'en-US';
        } else {
          vlang = 'es-CO';
        }
        var project = $scope.project;
        var category = $scope.category;
        if (project !== undefined
            && project !== ""
            && category !== undefined
            && category !== ""){
            $scope.response = "";
            $.gritter.add({
                title: event_title,
                text: event_wait,
                class_name: 'color info',
                sticky: false,
            });
            $(".loader").show();
            $scope.maxRecursiveCall = 5;
            eventualityFactory.getEvntByName(project, category).then(function(data){
                if(!data.error){
                    //CONFIGURACION DE TABLA
                    $scope.view.event = true;
                    for(var i = 0; i< data.data.length;i++){
                        switch (data.data[i].tipo) {
                            case "Autorización para ataque especial":
                                data.data[i].tipo = $translate.instant('event_formstack.type.auth_attack');
                                break;
                            case "Alcance difiere a lo aprobado":
                                data.data[i].tipo = $translate.instant('event_formstack.type.toe_differs');
                                break;
                            case "Aprobación de alta disponibilidad":
                                data.data[i].tipo = $translate.instant('event_formstack.type.high_approval');
                                break;
                            case "Insumos incorrectos o faltantes":
                                data.data[i].tipo = $translate.instant('event_formstack.type.incor_supplies');
                                break;
                            case "Cliente suspende explicitamente":
                                data.data[i].tipo = $translate.instant('event_formstack.type.explic_suspend');
                                break;
                            case "Cliente aprueba cambio de alcance":
                                data.data[i].tipo = $translate.instant('event_formstack.type.approv_change');
                                break;
                            case "Cliente cancela el proyecto/hito":
                                data.data[i].tipo = $translate.instant('event_formstack.type.cancel_proj');
                                break;
                            case "Cliente detecta ataque":
                                data.data[i].tipo = $translate.instant('event_formstack.type.det_attack');
                                break;
                            case "Otro":
                                data.data[i].tipo = $translate.instant('event_formstack.type.other');
                                break;
                            case "Ambiente no accesible":
                                data.data[i].tipo = $translate.instant('event_formstack.type.inacc_ambient');
                                break;
                            case "Ambiente inestable":
                                data.data[i].tipo = $translate.instant('event_formstack.type.uns_ambient');
                                break;
                            default:
                                data.data[i].tipo = $translate.instant('event_formstack.type.unknown');
                        }
                        switch (data.data[i].estado) {
                            case "Pendiente":
                                data.data[i].estado = $translate.instant('event_formstack.status.unsolve');
                                break;
                            case "Tratada":
                                data.data[i].estado = $translate.instant('event_formstack.status.solve');
                                break;
                            default:
                                data.data[i].estado = $translate.instant('event_formstack.status.unknown');
                        }
                    }
                    $("#eventualities").bootstrapTable('destroy');
                    $("#eventualities").bootstrapTable({data: data.data, locale: vlang});
                    $("#eventualities").bootstrapTable('refresh');
                    //MANEJO DEL UI
                    $("#search_section").show();
                    $('[data-toggle="tooltip"]').tooltip();
                    integrates.evntTotalize(data);
                    $.gritter.add({
                        title: event_title,
                        text: updated_title,
                        class_name: 'color success',
                        sticky: false,
                    });
                }else{
                    $scope.view.event = false;
                    Rollbar.error("Error: An error occurred searching events");
                     $.gritter.add({
                        title: 'Error',
                        text: data.message,
                        class_name: 'color danger',
                        sticky: false,
                    });
                }
            });
        }else{
            $scope.response = event_required ;
        }
    };

    $scope.init();
});
