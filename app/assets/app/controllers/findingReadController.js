/**
 * Crea el controlador para la lectura de vulnerabilidades por ID
 * @name findingReadController
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {integrates.findingFactory} findingFactory
 * @return {undefined}
 */
integrates.controller("findingReadController", function($scope, findingFactory, $stateParams) {
    $scope.init = function(){
        mixpanel.track(
        "ReadFinding", {
            "Email": userEmail,
            "FindingID": $scope.id
            }
        );
    };
    $("#search_section").hide();
    var id = $stateParams.id;
    $scope.vuln = {};
    $scope.linkUpdate = BASE.url + "dashboard#/vuln/update/?id=" + id;
    if(id !== undefined){
        id = id.replace(/[^0-9]+/g, "");
        $scope.id = id;
        findingFactory.getVulnById(id).then(function(response){
            if(!response.error){
                if(response.data == undefined) window.close();
                $.gritter.add({
                    title: 'Correcto!',
                    text: 'Hallazgo cargado',
                    class_name: 'color success',
                    sticky: false,
                });
                $("#search_section").fadeIn(200);
                $scope.vuln = response.data;
                if($scope.vuln.nivel == "General"){
                    $scope.esDetallado = "hide-detallado";
                    $scope.esGeneral = "show-detallado";
                }else{
                    $scope.esDetallado = "show-detallado";
                    $scope.esGeneral = "hide-detallado";
                }
                $scope.init();
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
        window.close();
    }
});
