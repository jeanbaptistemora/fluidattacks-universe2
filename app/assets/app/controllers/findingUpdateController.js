/**
 * Crea el controlador para la actualización de vulnerabilidades por ID
 * @name findingUpdateController 
 * @param {Object} $scope 
 * @param {Object} $uibModal
 * @param {integrates.findingFactory} findingFactory 
 * @return {undefined}
 */
integrates.controller("findingUpdateController", function($scope, $uibModal, findingFactory, $stateParams) {
    $("#search_section").hide();
    var id = $stateParams.id;
    $scope.vuln = {};
    if(id !== undefined){
        id = id.replace(/[^0-9]+/g, "?");
        if(id.indexOf("?") > -1) window.close();
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
                var data = response.data;
                try{
                    data.cardinalidad = parseInt(data.cardinalidad);
                    data.criticidad = parseFloat(data.criticidad);
                }catch(e){
                    data.cardinalidad = 0;
                    data.criticidad = 0;
                }
                $scope.vuln = data;
                if($scope.vuln.nivel == "General"){
                    $scope.esDetallado = "hide-detallado";
                    $scope.esGeneral = "show-detallado";
                }else{
                    $scope.esDetallado = "show-detallado";  
                    $scope.esGeneral = "hide-detallado";  
                }
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
    /**
     * Despliega la modal de ver editar hallazgo
     * @function openModalEditar
     * @member integrates.findingController
     * @return {undefined}
     */
    $scope.openModal = function(){
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'editar.html',
            windowClass: 'ver-modal',
            controller: function($scope, $uibModalInstance, currentVulnerability){
                /**
                 * Confirma la actualizacion del hallazgo
                 * @function okModal
                 * @member integrates.findingUpdateController
                 * @return {undefined}
                 */
                $scope.okModal = function(){
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
});