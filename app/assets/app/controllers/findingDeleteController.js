/**
 * Crea el controlador para la eliminación de vulnerabilidades por ID
 * @name findingDeleteController
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {integrates.findingFactory} findingFactory
 * @return {undefined}
 */
integrates.controller("findingDeleteController", function($scope, $uibModal, findingFactory, $stateParams) {
    $scope.init = function(){
        mixpanel.track(
        "DeleteFinding", {
            "Email": userEmail,
            "FindingID": $scope.id
            }
        );
    };
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
                $scope.vuln = data;
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
    /**
     * Despliega la modal de ver eliminar hallazgo
     * @function openModal
     * @member integrates.findingDeleteController
     * @return {undefined}
     */
    $scope.openModal = function(){
        if(!$scope.vuln.justificacion){
            $.gritter.add({
                title: 'Error!',
                text: "Debes ingresar una justificacion!",
                class_name: 'color warning',
                sticky: false,
            });
            return false;
        }
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'eliminar.html',
            windowClass: 'modal',
            controller: function($scope, $uibModalInstance, currentVulnerability){
                /**
                 * Confirma la eliminacion del hallazgo
                 * @function okModal
                 * @member integrates.findingDeleteController
                 * @return {undefined}
                 */
                $scope.okModal = function(){
                   $scope.vuln = currentVulnerability;
                   findingFactory.deleteVuln($scope.vuln).then(function(response){
                        if(!response.error){
                            $.gritter.add({
                                title: 'Correcto!',
                                text: 'Hallazgo eliminado, la ventana se cerrara en 5 segundos',
                                class_name: 'color success',
                                sticky: false,
                            });
                            $uibModalInstance.dismiss('cancel');
                            setTimeout('window.close();',5000);
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
                 * @member integrates.findingDeleteController
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
