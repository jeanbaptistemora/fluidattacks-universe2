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
                                                $state, $stateParams, $q,
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
        if(localStorage['lang'] === "en"){
          var vlang = 'en-US';
        } else {
          var vlang = 'es-CO';
        }
        $timeout(function() {
          $("#myProjectsTbl").bootstrapTable({
              locale: vlang,
              url: BASE.url+"get_myprojects",
              onClickRow: function(row, elem){
                  $state.go("ProjectNamed", {project: row.project});
                }
            });
        $("#myProjectsTbl").bootstrapTable("refresh");
      });
    };
    $scope.initMyEventualities = function(){
        if(localStorage['lang'] === "en"){
          var vlang = 'en-US';
        } else {
          var vlang = 'es-CO';
        }
        var aux = $xhr.get($q, BASE.url + "get_myevents", {});
        aux.then(function(response){
          for(var i = 0; i< response.data.length;i++){
             switch (response.data[i].tipo) {
               case "Autorización para ataque especial":
                 response.data[i].tipo = $translate.instant('event_formstack.type.auth_attack');;
                 break;
               case "Alcance difiere a lo aprobado":
                 response.data[i].tipo = $translate.instant('event_formstack.type.toe_differs');;
                 break;
               case "Aprobación de alta disponibilidad":
                 response.data[i].tipo = $translate.instant('event_formstack.type.high_approval');;
                 break;
               case "Insumos incorrectos o faltantes":
                 response.data[i].tipo = $translate.instant('event_formstack.type.incor_supplies');;
                 break;
               case "Cliente suspende explicitamente":
                 response.data[i].tipo = $translate.instant('event_formstack.type.explic_suspend');;
                 break;
               case "Cliente aprueba cambio de alcance":
                 response.data[i].tipo = $translate.instant('event_formstack.type.approv_change');;
                 break;
               case "Cliente cancela el proyecto/hito":
                 response.data[i].tipo = $translate.instant('event_formstack.type.cancel_proj');;
                 break;
               case "Cliente detecta ataque":
                 response.data[i].tipo = $translate.instant('event_formstack.type.det_attack');;
                 break;
               case "Otro":
                 response.data[i].tipo = $translate.instant('event_formstack.type.other');;
                 break;
               case "Ambiente no accesible":
                 response.data[i].tipo = $translate.instant('event_formstack.type.inacc_ambient');;
                 break;
               case "Ambiente inestable":
                 response.data[i].tipo = $translate.instant('event_formstack.type.uns_ambient');;
                 break;
               case "Insumos incorrectos o faltantes":
                 response.data[i].tipo = $translate.instant('event_formstack.type.incor_supplies');;
                 break;
               default:
                 response.data[i].tipo = $translate.instant('event_formstack.type.unknown');;
             }
          };
          $("#myEventsTbl").bootstrapTable({
              locale: vlang,
              data: response.data,
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
      });
    };
    $scope.init = function(){
        $scope.initMyProjects();
        $scope.initMyEventualities();
    };

    $scope.init();
});
