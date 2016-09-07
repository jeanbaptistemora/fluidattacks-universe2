integrates.vulnbynameFormatter = function(value, row, index){
    return '<div class="btn-group">' +
                '<button type="button" class="btn btn-default btnVer" ng-click="openModalVer('+index+')"><i class="glyphicon glyphicon-eye-open"></i></button>' +
                '<button type="button" class="btn btn-primary"><i class="glyphicon glyphicon-pencil"></i></button>' +
                '<button type="button" class="btn btn-warning"><i class="glyphicon glyphicon-trash"></i></button>' +
           '</div>';
};
integrates.calcCardinality = function(data){
    var cardinalidad = 0; 
    data.data.forEach(function(i){ cardinalidad+= parseInt(i.cardinalidad); });
    $("#total_cardinalidad").html(cardinalidad);
    $("#total_hallazgos").html(data.data.length);
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
integrates.controller("searchController", function($scope,$uibModal, searchFactory) {

    $scope.init = function(){
        $("#search_section").hide();
        $(".loader").hide();
    }
    /*
     *  Modal para ver un hallazgo 
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
                   searchFactory.updateVuln($scope.vuln).then(function(response){
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
                    searchFactory.deleteVuln($scope.vuln).then(function(response){
                        if(!response.error){
                            $.gritter.add({
                                title: 'Correcto!',
                                text: 'Hallazgo actualizado',
                                class_name: 'color success',
                                sticky: false,
                            });
                            //integrates.deleteVulnRow($scope.vuln);
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
     *  Funcion para consultar hallazgos
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
            searchFactory.getVulnByName(project).then(function(data){
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
            });;
        }else{
            $scope.response = "El nombre es obligatorio";
        }
    };

    document.onkeypress = function(ev){ 
        if(ev.keyCode === 13){
            if($('#project').is(':focus')){
                $scope.searchVulnByName();
            }        
        }
    }

    $scope.searchVulnByDate = function(){

    };

    $scope.searchEvntByName = function(){
        var project = $scope.project;
        if (project !== undefined && project !== ""){
            $scope.response = "";
            searchFactory.getEvntByName(project);
        }else{
            $scope.response = "El nombre es obligatorio";
        }
    };

    $scope.init();
});