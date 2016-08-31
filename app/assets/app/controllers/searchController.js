integrates.vulnbynameFormatter = function(value, row, index){
    return '<div class="btn-group">' +
                '<button type="button" class="btn btn-default btnVer" ng-click="openModalVer('+index+')"><i class="glyphicon glyphicon-eye-open"></i></button>' +
                '<button type="button" class="btn btn-primary"><i class="glyphicon glyphicon-pencil"></i></button>' +
                '<button type="button" class="btn btn-warning"><i class="glyphicon glyphicon-trash"></i></button>' +
           '</div>';
};
integrates.controller("searchController", function($scope,$uibModal, searchFactory) {

    $scope.init = function(){
        $("#search_section").hide();
        $(".loader").hide();
    }

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
        //console.log($scope.currentVulnerability);
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'ver.html',
            windowClass: 'ver-modal',
            controller: function($scope, $uibModalInstance, currentVulnerability){
                $scope.vuln = currentVulnerability;
                /*
                if($scope.vuln.amenaza == undefined) $scope.vuln.amenaza = "";
                if($scope.vuln.riesgo == undefined) $scope.vuln.riesgo = "";*/
                if($scope.vuln.nivel == "General"){
                    $scope.esDetallado = "hide-detallado";
                    $scope.rows = "4";
                    $scope.cols = "12";
                }else{
                    $scope.esDetallado = "show-detallado";  
                    $scope.rows = "3";
                    $scope.cols = "6";
                }
                
                $scope.closeModalAvance = function(){
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
                    var cardinalidad = 0; 
                    data.data.forEach(function(i){ cardinalidad+= parseInt(i.cardinalidad); });
                    
                    //CONFIGURACION DE TABLA
                    $("#vulnerabilities").bootstrapTable('destroy');
                    $("#vulnerabilities").bootstrapTable(data);
                    $("#vulnerabilities").bootstrapTable('refresh');
                    //MANEJO DEL UI
                    $("#total_cardinalidad").html(cardinalidad);
                    $("#total_hallazgos").html(data.data.length);
                    $("#search_section").show();
                    $('[data-toggle="tooltip"]').tooltip(); 
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