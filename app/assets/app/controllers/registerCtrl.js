/* eslint no-magic-numbers: ["error", { "ignore":[-1,0,1] }]*/
/* global
integrates, BASE, userEmail, mixpanel, projectData:true,
eventsData:true, findingData:true, angular, $window, Rollbar */
/* eslint no-shadow: ["error", { "allow": ["$scope"] }]*/
/**
 * @file registerCtrl.js
 * @author engineering@fluidattacks.com
 */
/**
 * Controller definition for user registration view.
 * @name registerController
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "registerCtrl",
  function registerCtrl (
    $scope,
    $state,
    $stateParams,
    $timeout,
    $translate,
    $uibModal,
    $window,
    registerFactory
  ) {
    $scope.loadDashboard = function loadDashboard () {
      const currentUrl = $window.location.toString();
      if (localStorage.getItem("url_inicio") === null) {
        $window.location = "dashboard";
      }
      else {
        let baseUrl = "";
        if (currentUrl.indexOf("localhost:8000") === -1) {
          if (currentUrl.indexOf(".integrates.env") === -1) {
            baseUrl = "https://fluidattacks.com/integrates/dashboard";
            const link = `${baseUrl}#${localStorage.getItem("url_inicio")}`;
            localStorage.clear();
            $window.location = link;
          }
          else {
            const dev = currentUrl.match("https://(.*).integrates")[1];
            baseUrl = `https://${dev}.integrates.env.fluidattacks.com/dashbo`;
            const link = `${baseUrl}ard#${localStorage.getItem("url_inicio")}`;
            localStorage.clear();
            $window.location = link;
          }
        }
        else {
          baseUrl = "https://localhost:8000/dashboard";
          const link = `${baseUrl}#${localStorage.getItem("url_inicio")}`;
          localStorage.clear();
          $window.location = link;
        }
      }
    };

    $scope.showAlreadyLoggedin = function showAlreadyLoggedin () {
      angular.element("#alreadyLoggedin").show();
      localStorage.clear();
    };

    $scope.showNotAuthorized = function showNotAuthorized () {
      angular.element("#notAuthorizedTxt").show();
      const currentUrl = $window.location.toString();
      if (currentUrl.indexOf("localhost:8000") === -1) {
        mixpanel.track("Registered User", {
          "Email":
          "{{ request.session.username }}"
        });
      }
    };

    $scope.showLegalNotice = function showLegalNotice () {
      const infoReq = registerFactory.getLoginInfo();
      infoReq.then((response) => {
        if (angular.isUndefined(response.data)) {
          location.reload();
        }
        else if (response.data.remember) {
          $scope.loadDashboard();
        }
        else {
          $uibModal.open({
            "animation": true,
            "backdrop": "static",
            "controller" ($scope, $uibModalInstance) {
              $scope.okModalNotice = function okModalNotice () {
                if (response.data.is_registered) {
                  try {
                    mixpanel.time_event("Logged out");
                  }
                  catch (err) {
                    const msg = "Couldn't track session length (Adblock)";
                    Rollbar.warning(`Warning: ${msg}`);
                  }
                  let remember = false;
                  if (angular.isDefined($scope.remember_accept_legal)) {
                    remember = $scope.remember_accept_legal;
                  }
                  const acceptReq = registerFactory.acceptLegal(remember);
                  acceptReq.then(() => {
                    $uibModalInstance.close();
                    $scope.loadDashboard();
                  });
                }
                else {
                  $uibModalInstance.close();
                  $scope.showNotAuthorized();
                }
              };
            },
            "keyboard": false,
            "resolve": {"done": true},
            "scope": $scope,
            "templateUrl": "legalNotice.html",
            "windowClass": "modal avance-modal"
          });
        }
      });
    };
    if (localStorage.getItem("showAlreadyLoggedin") === "1") {
      $scope.showAlreadyLoggedin();
    }
    else {
      $scope.showLegalNotice();
    }
  }
);
