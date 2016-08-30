
integrates.controller("searchController", function($scope,$uibModal, searchFactory) {

    $scope.init = function(){
        $("#search_section").hide();
        $(".loader").hide();
    }

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
                    $("#total_cardinalidad").html(cardinalidad);
                    $("#total_hallazgos").html(data.data.length);
                    $("#search_section").show();
                    $("#vulnerabilities").bootstrapTable(data);
                    $("#vulnerabilities").bootstrapTable('refresh');
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