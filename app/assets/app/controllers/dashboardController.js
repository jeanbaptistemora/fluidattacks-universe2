/**
 * @file dashboardController.js
 * @author engineering@fluid.la
 */
/**
 * Crea el controlador de las funciones del dashboard
 * @name eventualityController 
 * @param {Object} $scope 
 * @param {Object} $uibModal
 * @return {undefined}
 */
integrates.controller("dashboardController", function($scope, $uibModal, $translate) {
    /**
     * Redirecciona a un usuario para cerrar la sesion
     * @function logout
     * @member integrates.dashboardController
     * @return {undefined}
     */
    $scope.logout = function(){
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'logout.html',
            windowClass: 'modal avance-modal',
            controller: function($scope, $uibModalInstance){
                $scope.closeModalLogout = function(){
                    $uibModalInstance.dismiss('cancel');
                }
                $scope.okModalLogout = function(){
                    location = BASE.url + "logout";
                }
            },
            resolve: {
                done: true
            }
        });
    }
    /**
     * Redirecciona a un usuario para cerrar la sesion
     * @function logout
     * @member integrates.dashboardController
     * @return {undefined}
     */
    $scope.changeLang = function(langKey){
		if(localStorage['lang'] == "es"
			|| localStorage['lang'] == "en"){
			localStorage['lang'] = langKey;
		}
		$translate.use(localStorage['lang']);
        //location.reload(); check for lang cookie
    }
});
