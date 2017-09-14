/**
 * @file dashboardController.js
 * @author engineering@fluid.la
 */
/**
 * Crea el controlador de las funciones del dashboard
 * @name dashboardController 
 * @param {Object} $scope 
 * @param {Object} $uibModal
 * @return {undefined}
 */
integrates.controller("dashboardCtrl", function($scope, $uibModal, $timeout,
                                                $state, $stateParams,
                                                $translate, dashboardFtry) {
    /**
     * Redirecciona a un usuario para cerrar la sesion
     * @function logout
     * @member integrates.dashboardCtrl
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
     * Obtiene los proyectos asignados
     * @function changeLang
     * @member integrates.dashboardCtrl
     * @return {undefined}
     */

    /**
     * Cambia el lenguaje del dashboard
     * @function changeLang
     * @member integrates.dashboardCtrl
     * @return {undefined}
     */
    $scope.changeLang = function(langKey){
		if(langKey == "es"
			|| langKey == "en"){
			localStorage['lang'] = langKey;
		}
		$translate.use(localStorage['lang']);
    }
    $scope.initMyProjects = function(){
        $("#myProjectsTbl").bootstrapTable({
            url: BASE.url+"get_myprojects",
            onClickRow: function(row, elem){
                $state.go("SearchProject", {project: row.project});
            }
        });
        $("#myProjectsTbl").bootstrapTable("refresh");
    };
    $scope.initMyEventualities = function(){
        $("#myEventsTbl").bootstrapTable({
            url: BASE.url+"get_myevents",
            onClickRow: function(row, elem){
                var modalInstance = $uibModal.open({
                    animation: true,
                    templateUrl: 'ver.html',
                    windowClass: 'modal avance-modal',
                    controller: function($scope, data, $uibModalInstance){
                        $scope.evnt = data;
                        $scope.close = function(){
                            $uibModalInstance.close();
                        }
                    },
                    resolve: {
                        data: row
                    }
                });
            }
        });
        $("#myEventsTbl").bootstrapTable("refresh");
    };
    $scope.init = function(){
        $scope.initMyProjects();
        $scope.initMyEventualities();
    };

    $scope.init();
});
