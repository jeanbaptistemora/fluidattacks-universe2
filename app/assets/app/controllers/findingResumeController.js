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
    $scope.init = function(){
        $scope.colorPalette();
        $scope.finding = {};
        $scope.finding.id = $stateParams.id;
        $scope.loadFindingByID($scope.finding.id);
        $scope.list = {};
    };

    $scope.init();
});