integrates.afectacionFormatter = function(value, row, index){
    if (value.trim() == "")
        return "0";
    return value;
};
integrates.evntTotalize = function(data){
    var cardinalidad = 0; 
    //data.data.forEach(function(i){ cardinalidad+= parseInt(i.cardinalidad); });
    //$("#total_cardinalidad").html(cardinalidad);
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
integrates.updateVulnRow = function(row){
    var data = $("#eventualities").bootstrapTable("getData")
    for(var i=0; i< data.length;i++){
        if(data[i].id == row.id){
            data[i] = row;
            $("#eventualities").bootstrapTable("destroy");
            $("#eventualities").bootstrapTable({data: data});
            $("#eventualities").bootstrapTable("refresh");
            break;
        }
    }
    integrates.evntTotalize({data: data});
};


integrates.controller("eventualityController", function($scope,$uibModal, eventualityFactory) {
    $scope.init = function(){
        $("#search_section").hide();
        $(".loader").hide();
    }
    /*
     *  Modal para ver un hallazgo 
     */
    $scope.openModalVer = function(){
        var sel = $("#eventualities").bootstrapTable('getSelections');
        if(sel.length == 0){
            $.gritter.add({
                title: 'Error',
                text: 'Debes seleccionar una eventualidad',
                class_name: 'color warning',
                    sticky: false,
            });
            return false;
        }else{
            $scope.currentEventuality = sel[0];
        }
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
                    $uibModalInstance.dismiss('cancel');
                }
            },
            resolve: {
                currentEventuality: function(){
                    return $scope.currentEventuality;
                }
            }
        });
    };
    /*
     *  Modal para obtener el string del resumen de eventualidades 
     */
    $scope.openModalAvance = function(){
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'avance.html',
            windowClass: 'modal avance-modal',  
            controller: function($scope, $uibModalInstance){
                $scope.rows = $("#eventualities").bootstrapTable('getData');
                $scope.closeModalAvance = function(){
                    $uibModalInstance.dismiss('cancel');
                }
            },
            resolve: {
                ok: true
            }
        });
    };
    /*
     *  Modal para obtener el string del formulario de avance 
     */
    $scope.openModalEditar = function(){
        var sel = $("#eventualities").bootstrapTable('getSelections');
        if(sel.length == 0){
            $.gritter.add({
                title: 'Error',
                text: 'Debes seleccionar una eventualidad',
                class_name: 'color warning',
                sticky: false,
            });
            return false;
        }else{
            $scope.currentEventuality = sel[0];
        }
        
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
                   console.log($scope.evnt);
                   try{
                       if($scope.evnt.afectacion == undefined){
                           throw "negativo";
                       }
                       submit = true;
                   }catch(e){
                       $.gritter.add({
                            title: 'Correcto!',
                            text: 'La afectacion debe ser un numero positivo o cero',
                            class_name: 'color warning',
                            sticky: false,
                       });
                   }finally{
                       if(submit == false){
                           return false;
                       }
                   }

                   eventualityFactory.updateEvnt($scope.evnt).then(function(response){
                        if(!response.error){
                            $.gritter.add({
                                title: 'Correcto!',
                                text: 'Eventualidad actualizada',
                                class_name: 'color success',
                                sticky: false,
                            });
                            integrates.updateEvnt($scope.evnt);
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
                currentEventuality: function(){
                    return $scope.currentEventuality;
                }
            }
        });
    };
    /*
     * Buscar eventualidades de un proyecto por su nombre
     */
    $scope.searchEvntByName = function(){
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
            eventualityFactory.getEvntByName(project).then(function(data){
                if(!data.error){
                    //CONFIGURACION DE TABLA
                    $("#eventualities").bootstrapTable('destroy');
                    $("#eventualities").bootstrapTable(data);
                    $("#eventualities").bootstrapTable('refresh');
                    //MANEJO DEL UI
                    $("#search_section").show();
                    $('[data-toggle="tooltip"]').tooltip(); 
                    integrates.evntTotalize(data);
                }else{
                     $.gritter.add({
                        title: 'Error',
                        text: 'El proyecto no existe...',
                        class_name: 'color warning',
                        sticky: false,
                    });
                    $scope.searchEvntByName();
                }
            }).catch(function(fallback) {
                $.gritter.add({
                    title: 'Consultando',
                    text: 'Error de formstack...',
                    class_name: 'color warning',
                    sticky: false,
                });
                $scope.searchEvntByName();
            });
        }else{
            $scope.response = "El nombre es obligatorio";
        }
    };

    document.onkeypress = function(ev){ 
        if(ev.keyCode === 13){
            if($('#project').is(':focus')){
                $scope.searchEvntByName();
            }        
        }
    }

    $scope.init();
});