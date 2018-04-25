/* eslint no-magic-numbers: ["error", { "ignore":
                                  [-1,0,0.4,0.6,1,1.176,1.5,2,4,4.611,10,
                                  10.41,13,20,43.221,100,200,300,1000,3000] }]*/
/* eslint no-shadow: ["error", { "allow":
                                   ["$scope","$stateParams", "projectFtry"] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, projectData:true,
nonexploitLabel:true, totalHigLabel:true, $scope:true,explotable:true, i:true,
totalSegLabel:true, openLabel:true, partialLabel:true, $msg, integrates, j:true,
document, userName, userEmail, Rollbar, aux:true, json:true, eventsData:true, $,
closeLabel:true, mixPanelDashboard, win:true, window, Organization, userRole,
fieldsToTranslate, keysToTranslate
 */
/**
 * @file projectFindingsCtrl.js
 * @author engineering@fluidattacks.com
 */
/**
 * @function removeHour
 * @param {string} value Date of the finging with hour
 * @member integrates.registerCtrl
 * @return {string} Date without hour
 */
function removeHour (value) {
  if (value.indexOf(":") !== -1) {
    return value.split(" ")[0];
  }
  return value;
}

/**
 * @function labelState
 * @param {string} value Status of the finding
 * @member integrates.registerCtrl
 * @return {string} Html code for specific label
 */
function labelState (value) {
  if (value === "Cerrado") {
    return "<label class='label label-success' style='background-color: " +
           "#31c0be'>Cerrado</label>";
  }
  else if (value === "Closed") {
    return "<label class='label label-success' style='background-color: " +
           "#31c0be'>Closed</label>";
  }
  else if (value === "Abierto") {
    return "<label class='label label-danger' style='background-color: " +
           "#f22;'>Abierto</label>";
  }
  else if (value === "Open") {
    return "<label class='label label-danger' style='background-color: " +
           "#f22;'>Open</label>";
  }
  else if (value === "Parcialmente cerrado") {
    return "<label class='label label-info' style='background-color: " +
           "#ffbf00'>Parcialmente cerrado</label>";
  }
  return "<label class='label label-info' style='background-color: " +
         "#ffbf00'>Partially closed</label>";
}

/**
 * Controlador de vista de proyectos
 * @name ProjectCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @return {undefined}
 */
/** @export */
integrates.controller(
  "projectFindingsCtrl",
  function projectFindingsCtrl (
    $scope, $location,
    $uibModal, $timeout,
    $state, $stateParams,
    $translate, projectFtry
  ) {
    $scope.init = function init () {
      const projectName = $stateParams.project;
      const findingId = $stateParams.finding;
      $scope.userRole = userRole;

      $scope.isManager = userRole !== "customer";
      // Defaults para cambiar vistas
      $scope.view = {};
      $scope.view.project = false;
      $scope.view.finding = false;
      // Parametros de ruta
      if (typeof findingId !== "undefined") {
        $scope.findingId = findingId;
      }
      if (typeof projectName !== "undefined" &&
                projectName !== "") {
        $scope.project = projectName;
        $scope.search();
        const org = Organization.toUpperCase();
        const projt = projectName.toUpperCase();
        mixPanelDashboard.trackReports(
          "ProjectFindings",
          userName,
          userEmail,
          org,
          projt
        );
      }
      // Asigna el evento buscar al textbox search y tecla enter
      $scope.configKeyboardView();
      $scope.goUp();
      $scope.finding = {};
    };
    $scope.goUp = function goUp () {
      $("html, body").animate({"scrollTop": 0}, "fast");
    };
    $scope.alertHeader = function alertHeader (company, project) {
      const req = projectFtry.getAlerts(company, project);
      req.then((response) => {
        if (!response.error && response.data.length > 0) {
          if (response.data.status_act === "1") {
            let html = "<div class=\"alert alert-danger-2\">";
            html += "<strong>Atención! </strong>" +
                    `${response.data[0].message}</div>`;
            document.getElementById("header_alert").innerHTML = html;
          }
        }
      });
    };
    $scope.configKeyboardView = function configKeyboardView () {
      document.onkeypress = function onkeypress (ev) {
        // Buscar un proyecto
        if (ev.keyCode === 13) {
          if ($("#project").is(":focus")) {
            $scope.search();
          }
        }
      };
    };
    $scope.generateFullDoc = function generateFullDoc () {
      const projectName = $scope.project;
      const data = $("#vulnerabilities").bootstrapTable("getData");
      for (let cont = 0; cont < data.length - 1; cont++) {
        for (let incj = cont + 1; incj < data.length; incj++) {
          if (parseFloat(data[cont].criticidad) <
              parseFloat(data[incj].criticidad)) {
            const aux = data[cont];
            data[cont] = data[incj];
            data[incj] = aux;
          }
        }
      }
      let generateDoc = true;
      let json = {};
      try {
        json = data;
        generateDoc = true;
        const err = "error";
        // Remove indices
        json = JSON.stringify(JSON.parse(JSON.stringify(json)));
        if (typeof json === "undefined" || json === "") {
          throw err;
        }
        if (projectName.trim() === "") {
          throw err;
        }
      }
      catch (err) {
        Rollbar.error("Error: An error ocurred generating document", err);
        generateDoc = false;
      }
      if (generateDoc === false) {
        return false;
      }
      const req = projectFtry.ProjectDoc(projectName, json, "IT");
      req.then((response) => {
        if (!response.error) {
          let url = `${BASE.url}export_autodoc?project=${$scope.project}`;
          url += "&format=IT";
          if (navigator.userAgent.indexOf("Firefox") === -1) {
            $scope.downloadURL = url;
          }
          else {
            const win = window.open(url, "__blank");
          }
        }
        else if (response.error) {
          Rollbar.error("Error: An error ocurred generating document");
        }
      });
      $scope.downloadDoc();
      return true;
    };
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
    $scope.generatePDF = function generatePDF () {
      const projectName = $stateParams.project;
      const currentLang = localStorage.lang;
      const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
      const langpatt = new RegExp("^en|es$");
      if (prjpatt.test(projectName) &&
                langpatt.test(currentLang)) {
        const url = `${BASE.url}doc/${currentLang}/project/${projectName}`;
        if (navigator.userAgent.indexOf("Firefox") === -1) {
          $scope.downloadURL = url;
        }
        else {
          const win = window.open(url, "__blank");
        }
      }
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
    $scope.search = function search () {
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
      const projectName = $stateParams.project;
      const tableFilter = $scope.filter;
      const finding = $scope.findingId;
      if (typeof projectName === "undefined" ||
                projectName === "") {
        const attentionAt = $translate.instant("proj_alerts.attentTitle");
        const attentionAc = $translate.instant("proj_alerts.attent_cont");
        $msg.warning(attentionAc, attentionAt);
        return false;
      }
      if ($stateParams.project !== $scope.project) {
        $state.go("ProjectIndicators", {"project": $scope.project});
      }
      else if ($stateParams.project === $scope.project) {
        $scope.view.project = false;
        $scope.view.finding = false;

        /* Handling presentation button */
        const searchAt = $translate.instant("proj_alerts.search_title");
        const searchAc = $translate.instant("proj_alerts.search_cont");
        $msg.info(searchAc, searchAt);
        if (projectData.length > 0 &&
            projectData[0].proyecto_fluid.toLowerCase() ===
            $scope.project.toLowerCase()) {
          $scope.view.project = true;
          $scope.loadFindingContent(projectData, vlang);
        }
        else {
          const reqProject = projectFtry.projectByName(
            projectName,
            tableFilter
          );
          reqProject.then((response) => {
            $scope.view.project = true;
            if (!response.error) {
              // Tracking Mixpanel
              mixPanelDashboard.trackSearch(
                "SearchFinding",
                userEmail,
                projectName
              );
              if (response.data.length === 0) {
                $scope.view.project = false;
                $scope.view.finding = false;
                $msg.error($translate.instant("proj_alerts.not_found"));
              }
              else {
                projectData = response.data;
                $scope.loadFindingContent(projectData, vlang);
              }
            }
            else if (response.error) {
              $scope.view.project = false;
              $scope.view.finding = false;
              if (response.message === "Access denied") {
                Rollbar.warning("Warning: Access to project denied");
                $msg.error($translate.instant("proj_alerts.access_denied"));
              }
              else if (response.message === "Project masked") {
                Rollbar.warning("Warning: Project deleted");
                $msg.error($translate.instant("proj_alerts.project_deleted"));
              }
              else {
                Rollbar.warning("Warning: Project not found");
                $msg.error($translate.instant("proj_alerts.not_found"));
              }
            }
          });
        }
      }
      return true;
    };
    $scope.loadFindingContent = function loadFindingContent (datatest, vlang) {
      const org = Organization.toUpperCase();
      const projt = $stateParams.project.toUpperCase();
      $scope.alertHeader(org, projt);
      for (let cont = 0; cont < datatest.length; cont++) {
        for (let inc = 0; inc < fieldsToTranslate.length; inc++) {
          if (datatest[cont][fieldsToTranslate[inc]] in keysToTranslate) {
            datatest[cont][fieldsToTranslate[inc]] =
                  $translate.instant(keysToTranslate[
                    datatest[cont][fieldsToTranslate[inc]]
                  ]);
          }
        }
      }
      // CONFIGURACION DE TABLA
      $("#vulnerabilities").bootstrapTable("destroy");
      $("#vulnerabilities").bootstrapTable({
        "cookie": true,
        "cookieIdTable": "saveId",
        "data": datatest,
        "exportDataType": "all",
        "locale": vlang,
        "onClickRow" (row, elem) {
          $state.go("FindingDescription", {
            "id": row.id,
            "project": row.proyecto_fluid.toLowerCase()
          });
          $("#infoItem").addClass("active");
          $("#info").addClass("active");
          $("#cssv2Item").removeClass("active");
          $("#cssv2").removeClass("active");
          $("#trackingItem").removeClass("active");
          $("#tracking").removeClass("active");
          $("#evidenceItem").removeClass("active");
          $("#evidence").removeClass("active");
          $("#exploitItem").removeClass("active");
          $("#exploit").removeClass("active");
          // Tracking mixpanel
          mixPanelDashboard.trackFinding("ReadFinding", userEmail, row.id);
          $scope.currentScrollPosition = $(document).scrollTop();
        },
        "pageSize": 50
      });
      $("#vulnerabilities").bootstrapTable("refresh");
      // MANEJO DEL UI
      $("#search_section").show();
      $("[data-toggle=\"tooltip\"]").tooltip();

      if (typeof $stateParams.finding !== "undefined") {
        $scope.finding.id = $stateParams.finding;
        $scope.view.project = false;
        $scope.view.finding = false;
      }
      $scope.data = datatest;
    };
    $scope.openModalAvance = function openModalAvance () {
      const modalInstance = $uibModal.open({
        "animation": true,
        "controller" ($scope, $uibModalInstance) {
          const auxiliar = $("#vulnerabilities").bootstrapTable("getData");
          const data = auxiliar;
          for (let cont = 0; cont < data.length; cont++) {
            data[cont].atributos = 0;
            data[cont].link = `${window.location.href.split("project/")[0]}` +
                          `project/${data[cont].proyecto_fluid.toLowerCase()}` +
                          `/${data[cont].id}/description`;
            if (typeof data[cont].registros !== "undefined" &&
                data[cont].registros !== "") {
              data[cont].atributos = 1 + (data[cont].registros.match(/\n/g) ||
                                     []).length;
            }
          }
          for (let cont = 0; cont < data.length - 1; cont++) {
            for (let incj = cont + 1; incj < data.length; incj++) {
              if (parseFloat(data[cont].criticidad) <
                  parseFloat(data[incj].criticidad)) {
                const aux = data[cont];
                data[cont] = data[incj];
                data[incj] = aux;
              }
            }
          }
          $scope.rows = data;
          $scope.closeModalAvance = function closeModalAvance () {
            $uibModalInstance.close();
            $timeout(() => {
              $("#vulnerabilities").bootstrapTable("load", auxiliar);
            }, 100);
          };
        },
        "keyboard": false,
        "resolve": {"ok": true},
        "templateUrl": "avance.html",
        "windowClass": "modal avance-modal"
      });
    };
    $scope.urlIndicators = function urlIndicators () {
      $state.go("ProjectIndicators", {"project": $scope.project});
    };
    $scope.urlFindings = function urlFindings () {
      $state.go("ProjectFindings", {"project": $scope.project});
    };
    $scope.urlEvents = function urlEvents () {
      $state.go("ProjectEvents", {"project": $scope.project});
    };
    $scope.init();
  }
);
