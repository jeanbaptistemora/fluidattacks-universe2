/* eslint no-magic-numbers: ["error", { "ignore":[-1,3000] }]*/
/* eslint no-shadow: ["error", { "allow":
                                   ["$scope","$stateParams", "projectFtry"] }]*/
/* global
BASE, integrates, Organization, mixPanelDashboard, userName, userEmail, $,
Rollbar,
 */
/**
 * @file report-generator.js
 * @author engineering@fluidattacks.com
 */

/**
 * Controlador de vista de proyectos
 * @name reportGenerator
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @return {undefined}
 */
/** @export */
integrates.controller(
  "reportGenerator",
  function reportGenerator (
    $scope, $location,
    $uibModal, $timeout,
    $state, $stateParams,
    $translate, projectFtry
  ) {
    $scope.reportModal = function reportModal () {
      // Tracking mixpanel
      const orgName = Organization.toUpperCase();
      const projectName = $scope.project.toUpperCase();
      mixPanelDashboard.trackReports(
        "Reports",
        userName,
        userEmail,
        orgName,
        projectName
      );
      const modalInstance = $uibModal.open({
        "animation": true,
        "controller" ($scope, $uibModalInstance, $stateParams, projectFtry) {
          const projName = $stateParams.project;
          const currentLang = localStorage.lang;
          $scope.findingMatrizTechnicalXLSReport = function
          findingMatrizTechnicalXLSReport () {
            const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
            const langpatt = new RegExp("^en|es$");
            if (prjpatt.test(projName) &&
                            langpatt.test(currentLang)) {
              // Tracking mixpanel
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
                const win = window.open(url, "__blank");
              }
            }
          };
          $scope.findingMatrizTechnicalPDFReport = function
          findingMatrizTechnicalPDFReport () {
            const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
            const langpatt = new RegExp("^en|es$");
            if (prjpatt.test(projName) &&
                            langpatt.test(currentLang)) {
              // Tracking mixpanel
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
                const win = window.open(url, "__blank");
              }
            }
          };
          $("#hasPresentation").hide();
          $("#hasPresentationMsg").show();
          $scope.init = function init () {
            $("#hasPresentation").hide();
            $("#hasPresentationMsg").show();
            $.get(`${BASE.url}check_pdf/project/` +
                  `${$stateParams.project}`, (cont) => {
              if (!cont.error) {
                if (cont.data.enable) {
                  $("#hasPresentation").show();
                  $("#hasPresentationMsg").hide();
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
              // Tracking mixpanel
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
                const win = window.open(url, "__blank");
              }
            }
          };
          $scope.findingMatrizExecutivePDFReport = function
          findingMatrizExecutivePDFReport () {
            const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
            const langpatt = new RegExp("^en|es$");
            if (prjpatt.test(projName) &&
                            langpatt.test(currentLang)) {
              // Tracking mixpanel
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
                const win = window.open(url, "__blank");
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
      if (typeof $scope.downloadURL === "undefined") {
        $timeout($scope.downloadDoc, 3000);
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
