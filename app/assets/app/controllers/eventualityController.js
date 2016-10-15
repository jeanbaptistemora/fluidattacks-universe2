integrates.afectacionFormatter = function(value, row, index){
    if (value.trim() == "")
        return "0";
    return value;
};
integrates.evntTotalize = function(data){
    var cardinalidad = 0; 
    //data.data.forEach(function(i){ cardinalidad+= parseInt(i.cardinalidad); });
    //$("#total_cardinalidad").html(cardinalidad);
    $("#total_eventualidades").html(data.data.length);
};
integrates.updateVulnRow = function(row){
    var data = $("#vulnerabilities").bootstrapTable("getData")
    for(var i=0; i<data.length;i++){
        if(data[i].id == row.id){
            data[i] = row;
            $("#vulnerabilities").bootstrapTable("destroy");
            $("#vulnerabilities").bootstrapTable({data: data});
            $("#vulnerabilities").bootstrapTable("refresh");
            break;
        }
    }
    integrates.calcCardinality({data: data});
};

integrates.deleteVulnRow = function(row){
    alert(1);
    var data = $("#vulnerabilities").bootstrapTable("getData")
    var newData = [];
    for(var i=0; i<data.length;i++){
        if(data[i].id != row.id){
            newData.append(row);
        }
    }
    console.log(newData);
    $("#vulnerabilities").bootstrapTable("destroy");
    $("#vulnerabilities").bootstrapTable({data: newData});
    $("#vulnerabilities").bootstrapTable("refresh");
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
    /*
     *  Modal para obtener el string del formulario de avance 
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
    /*
     *  Modal para obtener el string del formulario de avance 
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
    /*
     *  Modal para obtener el string del formulario de avance 
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
                    //$uibModalInstance.dismiss('cancel');
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