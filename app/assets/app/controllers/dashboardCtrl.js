/* eslint no-shadow: ["error", { "allow": ["$scope"] }]*/
/* eslint no-magic-numbers: ["error", { "ignore":[-1,0,1] }]*/
/* global
integrates, $,   mixpanel, userMail, $xhr, Organization, userEmail, angular,
mixPanelDashboard, userName, projectData:true, eventsData:true, Rollbar, BASE,
findingData:true, fieldsToTranslate, keysToTranslate, modalInstance:true, $msg
*/
/**
 * @file dashboardController.js
 * @author engineering@fluidattacks.com
 */
/**
 * Crea el controlador de las funciones del dashboard
 * @name dashboardController
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "dashboardCtrl",
  function dashboardCtrl (
    $q,
    $scope,
    $state,
    $stateParams,
    $timeout,
    $translate,
    $uibModal
  ) {
    $scope.initMyProjects = function initMyProjects () {
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
      $timeout(() => {
        angular.element("#myProjectsTbl").bootstrapTable({
          "locale": vlang,
          "onClickRow" (row) {
            $state.go("ProjectIndicators", {"project": row.project});
          },
          "url": `${BASE.url}get_myprojects`
        });
        angular.element("#myProjectsTbl").bootstrapTable("refresh");
      });
    };

    /**
     * Redirecciona a un usuario para cerrar la sesion
     * @function logout
     * @member integrates.dashboardCtrl
     * @return {undefined}
     */
    $scope.logout = function logout () {
      $uibModal.open({
        "animation": true,
        "controller" ($scope, $uibModalInstance) {
          $scope.closeModalLogout = function closeModalLogout () {
            $uibModalInstance.close();
          };
          $scope.okModalLogout = function okModalLogout () {
            projectData = [];
            eventsData = [];
            findingData = {};
            window.location = `${BASE.url}logout`;
          };
        },
        "resolve": {"done": true},
        "templateUrl": "logout.html",
        "windowClass": "modal avance-modal"
      });
    };

    /**
     * Cambia el lenguaje del dashboard
     * @function changeLang
     * @param {string} langKey Language key set by the user
     * @member integrates.dashboardCtrl
     * @return {undefined}
     */
    $scope.changeLang = function changeLang (langKey) {
      if (langKey === "es" || langKey === "en") {
        localStorage.lang = langKey;
      }
      $translate.use(localStorage.lang);
      mixpanel.identify(userEmail);
      mixpanel.people.set({"$Language": localStorage.lang});
      location.reload();
    };
    $scope.initMyEventualities = function initMyEventualities () {
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
      const aux = $xhr.get($q, `${BASE.url}get_myevents`, {});
      aux.then((response) => {
        if (typeof response.data === "undefined") {
          location.reload();
        }
        for (let cont = 0; cont < response.data.length; cont++) {
          if (response.data[cont].tipo in keysToTranslate) {
            response.data[cont].tipo =
                  $translate.instant(keysToTranslate[response.data[cont].tipo]);
          }
        }
        angular.element("#myEventsTbl").bootstrapTable({
          "data": response.data,
          "locale": vlang,
          "onClickRow" (row) {
            $uibModal.open({
              "animation": true,
              "controller" ($scope, data, $uibModalInstance) {
                $scope.evnt = data;
                // Tracking mixpanel
                const org = Organization.toUpperCase();
                const projt = $scope.evnt.proyecto_fluid.toUpperCase();
                mixPanelDashboard.trackReadEventuality(
                  userName,
                  userEmail,
                  org,
                  projt,
                  $scope.evnt.id
                );
                $scope.close = function close () {
                  $uibModalInstance.close();
                };
              },
              "resolve": {"data": row},
              "templateUrl": "ver.html",
              "windowClass": "modal avance-modal"
            });
          }
        });
        angular.element("#myEventsTbl").bootstrapTable("refresh");
      });
    };
    $scope.init = function init () {
      $scope.initMyProjects();
      $scope.initMyEventualities();
    };
    $scope.init();
  }
);
