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
 * @param {Object} ngNotify
 * @return {undefined}
 */
integrates.controller("FindingResumeController", function($scope, $stateParams,
                                                          $uibModal, $translate,
                                                          ngNotify, findingFactory) {
    $scope.headerBuilding = function(){
        //console.log($scope.finding);
        $scope.header = {};
        $scope.header.findingTitle = $scope.finding.hallazgo;
        $scope.header.findingType = $scope.finding.tipo_prueba;
        $scope.header.findingRisk = "";
        $scope.header.findingState = $scope.finding.estado;
        $scope.header.findingValue = $scope.finding.criticidad;
        var findingValue = parseFloat($scope.finding.criticidad);
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

        if($scope.header.findingState == "Abierto"){
            $scope.header.findingStateColor = $scope.colors.critical;
        }else if($scope.header.findingState == "Parcialmente cerrado"){
            $scope.header.findingStateColor = $scope.colors.moderate;
        }else{
            $scope.header.findingStateColor = $scope.colors.ok;
        }

        $scope.header.findingCount = $scope.finding.cardinalidad;
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
                    $scope.informationTab();
                }else{
                    $.gritter.add({
                        title: 'Error!', text: response.message,
                        class_name: 'color warning', sticky: false,
                    });
                    window.close();
                }
            });
        }
    };
    $scope.colorPalette = function(){
        $scope.colors = {};
        $scope.colors.critical = "background-color: #f12;";  //red
        $scope.colors.moderate = "background-color: #f72;";  //orange
        $scope.colors.tolerable = "background-color: #fd2;"; //yellow
        $scope.colors.ok = "background-color: #008000;"; //green
    };
    $scope.calculteCSSv2 = function(){
        var ImpCon = parseFloat($scope.finding.impacto_confidencialidad.split(" | ")[0]);
        var ImpInt = parseFloat($scope.finding.impacto_integridad.split(" | ")[0]);
        var ImpDis = parseFloat($scope.finding.impacto_disponibilidad.split(" | ")[0]);
        var AccCom = parseFloat($scope.finding.complejidad_acceso.split(" | ")[0]);
        var AccVec = parseFloat($scope.finding.vector_acceso.split(" | ")[0]);
        var Auth = parseFloat($scope.finding.autenticacion.split(" | ")[0]);
        var Explo = parseFloat($scope.finding.explotabilidad.split(" | ")[0]);
        var Resol = parseFloat($scope.finding.nivel_resolucion.split(" | ")[0]);
        var Confi = parseFloat($scope.finding.nivel_confianza.split(" | ")[0]);
        var BaseScore = (((0.6*(10.41*(1-(1-ImpCon)*(1-ImpInt)*(1-ImpDis))))+(0.4*(20*AccCom*Auth*AccVec))-1.5)*1.176);
        Temporal = BaseScore * Explo * Resol * Confi;
        CVSSGeneral = Temporal;
        $scope.finding.cssv2base = BaseScore.toFixed(1);
        $scope.finding.criticidad = Temporal.toFixed(1);
    };
    $scope.dropDownList = function(){
        $scope.list = {};
        $scope.list.finding_type = finding_type;
        $scope.list.finding_test_type = finging_test_type;
        $scope.list.categories = categories;
        $scope.list.probability = probabilities;
        $scope.list.actor = actor;
        $scope.list.scenario = scenario;
        $scope.list.accessVector = accessVector;
        $scope.list.accessComplexity = accessComplexity;
        $scope.list.authentication = authentication;
        $scope.list.confidenciality = confidenciality;
        $scope.list.integrity = integrity;
        $scope.list.availability = availability;
        $scope.list.explotability = explotability;
        $scope.list.resolutionLevel = resolutionLevel;
        $scope.list.realiabilityLevel = realiabilityLevel;
    };
    $scope.informationTab = function(){
        $scope.dropDownList();
        $scope.finding.cardinalidad = parseInt($scope.finding.cardinalidad);
        $scope.finding.criticidad = parseFloat($scope.finding.criticidad);
        $scope.calculteCSSv2();
        if($scope.finding.nivel == "Detallado"){
            $scope.esDetallado = "show-detallado";
            $scope.esGeneral = "hide-detallado";
            $scope.calculateSeveridad();
        }else{
            $scope.esDetallado = "hide-detallado";
            $scope.esGeneral = "show-detallado";
        }
    };
    $scope.calculateSeveridad = function(){
        if(!isNaN($scope.finding.severidad)){
            var severidad = parseFloat($scope.finding.severidad);
            if (severidad < 0 || severidad > 5){
                ngNotify.set("La severidad debe ser un numero de 0 a 5", "error");
                return false;
            }
            try{
                var prob = $scope.finding.probabilidad;
                var severidad = $scope.finding.severidad;
                prob = prob.split("%")[0];
                prob = parseFloat(prob)/100.0;
                severidad = parseFloat(severidad);
                var vRiesgo = prob*severidad;
                if(vRiesgo >= 3){
                    $scope.finding.valor_riesgo = "(:r) Critico".replace(":r", vRiesgo.toFixed(1));
                }else if(vRiesgo >= 2 && vRiesgo < 3){
                    $scope.finding.valor_riesgo = "(:r) Moderado".replace(":r", vRiesgo.toFixed(1));
                }else{
                    $scope.finding.valor_riesgo = "(:r) Tolerable".replace(":r", vRiesgo.toFixed(1));
                }
            }catch(e){
                    $scope.finding.valor_riesgo = "";
            }
        }else{
            ngNotify.set("La severidad debe ser un numero de 0 a 5", "error");
        }
    };
    $scope.blockingUpdates = function(){
        if(userRole == "analyst"){
            $("textarea").attr("disabled", true);
            $("select").attr("disabled", true);
            $("input").attr("disabled", true);
            $scope.colsBack = "col-md-4 col-md-offset-2";
            $scope.colsEnable = "col-md-4";
            $scope.enable = "fl-visible";
            $scope.updateable = "fl-hidden";
        }else{
            $("textarea").attr("disabled", true);
            $("select").attr("disabled", true);
            $("input").attr("disabled", true);
            $scope.colsBack = "col-md-4 col-md-offset-4";
            $scope.enable = "fl-hidden";
            $scope.updateable = "fl-hidden";
        }
        $("#proyecto_fluid").attr("disabled", true);
        $("#proyecto_cliente").attr("disabled", true);
        $("#valor_riesgo").attr("disabled", true);
        $("#cssv2base").attr("disabled", true);
        $("#criticidad").attr("disabled", true);
    };

    $scope.enableUpdate = function(){
        if(userRole == "analyst"){
            $("textarea").attr("disabled", false);
            $("select").attr("disabled", false);
            $("input").attr("disabled", false);
        }
        $scope.colsBack = "col-md-4";
        $scope.colsUpdateable = "col-md-4";
        $scope.colsEnable = "col-md-4";
        $scope.updateable = "fl-visible";
        $("#proyecto_fluid").attr("disabled", true);
        $("#proyecto_cliente").attr("disabled", true);
        $("#valor_riesgo").attr("disabled", true);
        $("#cssv2base").attr("disabled", true);
        $("#criticidad").attr("disabled", true);
    }
    /**
     * Despliega la modal de ver editar hallazgo
     * @function openModalEditar
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.updateFinding = function(){
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'update.html',
                windowClass: 'ver-modal',
                controller: function($scope, $uibModalInstance, currentVulnerability){
                    /**
                     * Confirma la actualizacion del hallazgo
                     * @function okModal
                     * @member integrates.findingUpdateController
                     * @return {undefined}
                     */
                    $scope.okModal = function(){
                        /*
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
                        */
                    }
                    /**
                     * Cierra la modal
                     * @function closeModal
                     * @member integrates.findingUpdateController
                     * @return {undefined}
                     */
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

    $scope.init = function(){
        $scope.colorPalette();
        $scope.finding = {};
        $scope.finding.id = $stateParams.id;
        $scope.loadFindingByID($scope.finding.id);
        $scope.blockingUpdates();
    };

    $scope.init();
});
