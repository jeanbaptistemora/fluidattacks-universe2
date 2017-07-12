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
                                                          $uibModal, $translate) {
    $scope.init = function(){
        $scope.finding = {};
        $scope.finding.id = $stateParams.id;
        if(isNaN($scope.finding.id)) //avoid fake paths or id
            window.close();
    };

    $scope.init();
});