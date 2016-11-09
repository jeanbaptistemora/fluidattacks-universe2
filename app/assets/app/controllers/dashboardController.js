integrates.controller("dashboardController", function($scope, $uibModal) {
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
                    location = "/logout";
                }
            },
            resolve: {
                done: true
            }
        });
    }
});