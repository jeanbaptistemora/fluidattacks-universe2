/* eslint-disable angular/document-service */
/* eslint no-magic-numbers: ["error", { "ignore":[-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow":
                                   ["$scope","$stateParams", "projectFtry"] }]*/
/* global
BASE, integrates, Organization, mixPanelDashboard, userName, userEmail, $,
Rollbar, angular,$window */
/**
 * @file reportGeneratorCtrl.js
 * @author engineering@fluidattacks.com
 */

/**
 * Controller definition for report generator modal.
 * @name reportGeneratorCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "reportGeneratorCtrl",
  function reportGeneratorCtrl (
    $location,
    $scope,
    $timeout,
    $uibModal,
    $window
  ) {
    $scope.reportModal = function reportModal () {
      // Mixpanel tracking
      const orgName = Organization.toUpperCase();
      const projectName = $scope.project.toUpperCase();
      mixPanelDashboard.trackReports(
        "Reports",
        userName,
        userEmail,
        orgName,
        projectName
      );
      $uibModal.open({
        "animation": true,
        "controller" ($scope, $uibModalInstance, $stateParams) {
          const projName = $stateParams.project;
          const currentLang = localStorage.lang;
          $scope.findingMatrizTechnicalXLSReport = function
          findingMatrizTechnicalXLSReport () {
            const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
            const langpatt = new RegExp("^en|es$");
            if (prjpatt.test(projName) &&
                            langpatt.test(currentLang)) {
              // Mixpanel tracking
              mixPanelDashboard.trackReports(
                "TechnicalReportXLS",
                userName,
                userEmail,
                orgName,
                projName
              );
              const url = `${BASE.url}xls/${currentLang}/project/${projName}`;
              if (navigator.userAgent.indexOf("Firefox") === -1) {
                const downLink = document.createElement("a");
                downLink.target = "_blank";
                downLink.href = url;
                downLink.click();
              }
              else {
                $window.open(url, "__blank");
              }
            }
          };
          $scope.findingMatrizTechnicalPDFReport = function
          findingMatrizTechnicalPDFReport () {
            const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
            const langpatt = new RegExp("^en|es$");
            if (prjpatt.test(projName) &&
                            langpatt.test(currentLang)) {
              // Mixpanel tracking
              mixPanelDashboard.trackReports(
                "TechnicalReportPDF",
                userName,
                userEmail,
                orgName,
                projName
              );
              const url = `${BASE.url}pdf/${currentLang}/` +
                          `project/${projName}/tech/`;
              if (navigator.userAgent.indexOf("Firefox") === -1) {
                const downLink = document.createElement("a");
                downLink.target = "_blank";
                downLink.href = url;
                downLink.click();
              }
              else {
                $window.open(url, "__blank");
              }
            }
          };
          angular.element("#hasPresentation").hide();
          angular.element("#hasPresentationMsg").show();
          $scope.init = function init () {
            angular.element("#hasPresentation").hide();
            angular.element("#hasPresentationMsg").show();
            $.get(`${BASE.url}check_pdf/project/` +
                  `${$stateParams.project}`, (cont) => {
              if (!cont.error) {
                if (cont.data.enable) {
                  angular.element("#hasPresentation").show();
                  angular.element("#hasPresentationMsg").hide();
                }
              }
              else if (cont.error) {
                Rollbar.error("Error: An error ocurred " +
                              "generating the executive report");
              }
            });
          };
          $scope.findingMatrizExecutivePDFPresentation = function
          findingMatrizExecutivePDFPresentation () {
            const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
            const langpatt = new RegExp("^en|es$");
            if (prjpatt.test(projName) &&
                            langpatt.test(currentLang)) {
              // Mixpanel tracking
              mixPanelDashboard.trackReports(
                "ExecutivePDFPresentation",
                userName,
                userEmail,
                orgName,
                projName
              );
              const url = `${BASE.url}pdf/${currentLang}/project/` +
                          `${projName}/presentation/`;
              if (navigator.userAgent.indexOf("Firefox") === -1) {
                const downLink = document.createElement("a");
                downLink.target = "_blank";
                downLink.href = url;
                downLink.click();
              }
              else {
                $window.open(url, "__blank");
              }
            }
          };
          $scope.findingMatrizExecutivePDFReport = function
          findingMatrizExecutivePDFReport () {
            const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
            const langpatt = new RegExp("^en|es$");
            if (prjpatt.test(projName) &&
                            langpatt.test(currentLang)) {
              // Mixpanel tracking
              mixPanelDashboard.trackReports(
                "ExecutivePDFReport",
                userName,
                userEmail,
                orgName,
                projName
              );
              const url = `${BASE.url}pdf/${currentLang}` +
                          `/project/${projName}/executive/`;
              if (navigator.userAgent.indexOf("Firefox") === -1) {
                const downLink = document.createElement("a");
                downLink.target = "_blank";
                downLink.href = url;
                downLink.click();
              }
              else {
                $window.open(url, "__blank");
              }
            }
          };
          $scope.closeModalAvance = function closeModalAvance () {
            $uibModalInstance.close();
          };
          $scope.init();
        },


        "keyboard": false,
        "resolve": {"ok": true},
        "size": "lg",
        "templateUrl": "reportModal.html",
        "windowClass": "modal avance-modal"
      });
    };

    $scope.downloadDoc = function downloadDoc () {
      const TIMEOUT = 3000;
      if (angular.isUndefined($scope.downloadURL)) {
        $timeout($scope.downloadDoc, TIMEOUT);
      }
      else {
        const downLink = document.createElement("a");
        downLink.target = "_blank";
        downLink.href = $scope.downloadURL;
        downLink.click();
      }
    };
  }
);
