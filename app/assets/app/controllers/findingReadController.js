/**
 * Crea el controlador para la lectura de vulnerabilidades por ID
 * @name findingReadController
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {integrates.findingFactory} findingFactory
 * @return {undefined}
 */
integrates.controller("findingReadController", function($scope, findingFactory, $stateParams) {
    $("#search_section").hide();
    var id = $stateParams.id;
    $scope.vuln = {};
    $scope.linkUpdate = BASE.url + "dashboard#!/vuln/update/?id=" + id;
    if(id !== undefined){
        id = id.replace(/[^0-9]+/g, "?");
        $scope.id = id;
        findingFactory.getVulnById(id).then(function(response){
            if(!response.error){

                if(response.data == undefined){
                    console.log(response);
                }
                $.gritter.add({
                    title: 'Correcto!',
                    text: 'Hallazgo cargado',
                    class_name: 'color success',
                    sticky: false,
                });
                $("#search_section").fadeIn(200);
                $scope.vuln = response.data;
                if($scope.vuln.nivel == "Detallado"){
                    $scope.esDetallado = "show-detallado";
                    $scope.esGeneral = "hide-detallado";
                    try{
                        var prob = $scope.vuln.probabilidad;
                        var severidad = $scope.vuln.severidad;
                        prob = prob.split("%")[0];
                        prob = parseFloat(prob)/100.0;
                        severidad = parseFloat(severidad);
                        var vRiesgo = prob*severidad;   
                        if(vRiesgo >= 3){
                            $scope.vuln.vRiesgo = "Critico";
                        }else if(vRiesgo >= 2 && vRiesgo < 3){
                            $scope.vuln.vRiesgo = "Moderado";
                        }else{
                            $scope.vuln.vRiesgo = "Tolerable";
                        }
                    }catch(e){
                        $scope.vuln.vRiesgo = "";
                    }
                }else{
                    $scope.esDetallado = "hide-detallado";
                    $scope.esGeneral = "show-detallado";
                }
		mixPanelDashboard.trackReadFinding(id);
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
        //window.close();
    }
});
