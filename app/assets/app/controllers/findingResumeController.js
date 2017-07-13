/**
 * @file findingResumeController.js
 * @author engineering@fluid.la
 */
/**
 * Funciones para administrar el UI del resumen de un hallazgo
 * @name findingResumeController 
 * @param {Object} $scope 
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $translate
 * @return {undefined}
 */
integrates.controller("FindingResumeController", function($scope, $stateParams,
                                                          $uibModal, $translate,
                                                          findingFactory) {                                                            
    $scope.headerBuilding = function(){
        console.log($scope.finding);
        $scope.header = {};
        $scope.header.findingTitle = $scope.finding.hallazgo;
        $scope.header.findingType = $scope.finding.tipo_prueba;
        $scope.header.findingRisk = "";
        $scope.header.findingValue = $scope.finding.criticidad;
        var findingValue = parseFloat($scope.finding.criticidad);
        console.log(parseFloat(findingValue));
        if(findingValue >= 7){
            $scope.header.findingValueDescription = " Alto";
            $scope.header.findingValueColor = $scope.colors.critical;
        }else if(findingValue >= 4 && findingValue <= 6.9){
            $scope.header.findingValueDescription = " Moderado";
            $scope.header.findingValueColor = $scope.colors.moderate;
        }else{
            $scope.header.findingValueDescription = " Tolerable";
            $scope.header.findingValueColor = $scope.colors.tolerable;
        }
        $scope.header.findingCount = $scope.finding.cardinalidad;
        console.log($scope.header.findingValueDescription);
    };                                                           
    $scope.loadFindingByID = function(id){
        if(isNaN(id)){
           window.close();  //avoid fake paths or id
        }else{
            var req = findingFactory.getVulnById(id);
            req.then(function(response){
                if(!response.error){
                    $scope.finding = response.data;
                    $scope.headerBuilding();
                    if($scope.finding.nivel == "Detallado"){
                        $scope.esDetallado = "show-detallado";
                        $scope.esGeneral = "hide-detallado";
                        try{
                            var prob = $scope.finding.probabilidad;
                            var severidad = $scope.finding.severidad;
                            prob = prob.split("%")[0];
                            prob = parseFloat(prob)/100.0;
                            severidad = parseFloat(severidad);
                            var vRiesgo = prob*severidad; 
                            if(vRiesgo >= 3){
                                $scope.finding.valor_riesgo = "Critico";
                            }else if(vRiesgo >= 2 && vRiesgo < 3){
                                $scope.finding.valor_riesgo = "Moderado";
                            }else{
                                $scope.finding.valor_riesgo = "Tolerable";
                            }
                        }catch(e){
                            $scope.finding.valor_riesgo = "";
                            console.log("excepcion" + e);
                        }
                    }else{
                        $scope.esDetallado = "hide-detallado";
                        $scope.esGeneral = "show-detallado";
                    } 
                    //$scope.finding.impacto_confidencialidad = $scope.finding.impacto_confidencialidad.split(" | ")[0];
                    //$scope.finding.impacto_integridad = $scope.finding.impacto_integridad.split(" | ")[0];
                    //$scope.finding.impacto_disponibilidad = $scope.finding.impacto_disponibilidad.split(" | ")[0];    
                }else{
                    $.gritter.add({
                        title: 'Error!', text: response.message,
                        class_name: 'color warning', sticky: false,
                    });
                }
            });
        }
    };
    $scope.colorPalette = function(){
        $scope.colors = {};
        $scope.colors.critical = "background-color: #f12;";  //red
        $scope.colors.moderate = "background-color: #f72;";  //orange
        $scope.colors.tolerable = "background-color: #ff2;"; //yellow
    };
    /*
     * Add CSSV2.js data to $scope lists
     */
    $scope.dropDownList = function(){
        $scope.list = {};
        $scope.list.finding_type = finding_type;
        $scope.list.finding_test_type = finging_test_type;
        $scope.list.actor = actor;
        $scope.list.scenario = scenario;
        $scope.list.accessVector = accessVector;
        $scope.list.accessComplexity = accessComplexity;
        $scope.list.authentication = authentication;
        $scope.list.confidenciality = confidenciality;
        $scope.list.integrity = integrity;
        $scope.list.disponibility = disponibility;
        $scope.list.explotability = explotability;
        $scope.list.resolutionLevel = resolutionLevel;
        $scope.list.realiabilityLevel = realiabilityLevel;
    };
    $scope.init = function(){
        $scope.colorPalette();
        $scope.finding = {};
        $scope.finding.id = $stateParams.id;
        $scope.loadFindingByID($scope.finding.id);
        $scope.dropDownList();
    };

    $scope.init();
});