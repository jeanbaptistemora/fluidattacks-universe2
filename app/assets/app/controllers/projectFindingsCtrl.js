
/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,0.4,0.6,1,1.176,1.5,2,4,4.611,10,10.41,13,20,43.221,100,200,300,1000,3000] }]*/
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams", "projectFtry"] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, nonexploitLabel:true, totalHigLabel:true, $scope:true,
explotable:true, totalSegLabel:true, openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg, userName,
userEmail, Rollbar, aux:true, json:true, closeLabel:true, mixPanelDashboard, win:true, window, Organization, projectData:true, eventsData:true,
i:true, j:true
 * @file ProjectCtrl.js
 * @author engineering@fluidattacks.com
 */
/* Table Formatter */
/**
 * Function removeHour return date without hour
 */
function removeHour (value, row, index) {
  if (value.indexOf(":") !== -1) {
    return value.split(" ")[0];
  }
  return value;
}

/**
 * Function labelState return html code for specific label
 */
function labelState (value, row, index) {
  if (value === "Cerrado") {
    return "<label class='label label-success' style='background-color: #31c0be'>Cerrado</label>";
  }
  else if (value === "Closed") {
    return "<label class='label label-success' style='background-color: #31c0be'>Closed</label>";
  }
  else if (value === "Abierto") {
    return "<label class='label label-danger' style='background-color: #f22;'>Abierto</label>";
  }
  else if (value === "Open") {
    return "<label class='label label-danger' style='background-color: #f22;'>Open</label>";
  }
  else if (value === "Parcialmente cerrado") {
    return "<label class='label label-info' style='background-color: #ffbf00'>Parcialmente cerrado</label>";
  }
  return "<label class='label label-info' style='background-color: #ffbf00'>Partially closed</label>";
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
      const projectAux = $stateParams.project;
      const project = projectAux;
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
      if (typeof project !== "undefined" &&
                project !== "") {
        $scope.project = project;
        $scope.search();
        const org = Organization.toUpperCase();
        const projt = project.toUpperCase();
        mixPanelDashboard.trackReports("ProjectFindings", userName, userEmail, org, projt);
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
            html += `<strong>Atención! </strong>${response.data[0].message}</div>`;
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
      const projectAux = $scope.project;
      const project = projectAux;
      const data = $("#vulnerabilities").bootstrapTable("getData");
      for (let cont = 0; cont < data.length - 1; cont++) {
        for (let incj = cont + 1; incj < data.length; incj++) {
          if (parseFloat(data[cont].criticidad) < parseFloat(data[incj].criticidad)) {
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
        if (project.trim() === "") {
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
      const req = projectFtry.ProjectDoc(project, json, "IT");
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
      const org = Organization.toUpperCase();
      const projt = $scope.project.toUpperCase();
      mixPanelDashboard.trackReports("Reports", userName, userEmail, org, projt);
      const modalInstance = $uibModal.open({
        "animation": true,
        "controller" ($scope, $uibModalInstance, $stateParams, projectFtry) {
          $scope.findingMatrizTechnicalXLSReport = function findingMatrizTechnicalXLSReport () {
            const projectAux = $stateParams.project;
            const project = projectAux;
            const langAux = localStorage.lang;
            const lang = langAux;
            const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
            const langpatt = new RegExp("^en|es$");
            if (prjpatt.test(project) &&
                            langpatt.test(lang)) {
              // Tracking mixpanel
              mixPanelDashboard.trackReports("TechnicalReportXLS", userName, userEmail, org, projt);
              const url = `${BASE.url}xls/${lang}/project/${project}`;
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
          $scope.findingMatrizTechnicalPDFReport = function findingMatrizTechnicalPDFReport () {
            const projectAux = $stateParams.project;
            const project = projectAux;
            const langAux = localStorage.lang;
            const lang = langAux;
            const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
            const langpatt = new RegExp("^en|es$");
            if (prjpatt.test(project) &&
                            langpatt.test(lang)) {
              // Tracking mixpanel
              mixPanelDashboard.trackReports("TechnicalReportPDF", userName, userEmail, org, projt);
              const url = `${BASE.url}pdf/${lang}/project/${project}/tech/`;
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
            $.get(`${BASE.url}check_pdf/project/${$stateParams.project}`, (cont) => {
              if (!cont.error) {
                if (cont.data.enable) {
                  $("#hasPresentation").show();
                  $("#hasPresentationMsg").hide();
                }
              }
              else if (cont.error) {
                Rollbar.error("Error: An error ocurred generating the executive report");
              }
            });
          };
          $scope.findingMatrizExecutivePDFPresentation = function findingMatrizExecutivePDFPresentation () {
            const projectAux = $stateParams.project;
            const project = projectAux;
            const langAux = localStorage.lang;
            const lang = langAux;
            const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
            const langpatt = new RegExp("^en|es$");
            if (prjpatt.test(project) &&
                            langpatt.test(lang)) {
              // Tracking mixpanel
              mixPanelDashboard.trackReports("ExecutivePDFPresentation", userName, userEmail, org, projt);
              const url = `${BASE.url}pdf/${lang}/project/${project}/presentation/`;
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
          $scope.findingMatrizExecutivePDFReport = function findingMatrizExecutivePDFReport () {
            const projectAux = $stateParams.project;
            const project = projectAux;
            const langAux = localStorage.lang;
            const lang = langAux;
            const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
            const langpatt = new RegExp("^en|es$");
            if (prjpatt.test(project) &&
                            langpatt.test(lang)) {
              // Tracking mixpanel
              mixPanelDashboard.trackReports("ExecutivePDFReport", userName, userEmail, org, projt);
              const url = `${BASE.url}pdf/${lang}/project/${project}/executive/`;
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
      const projectAux = $stateParams.project;
      const project = projectAux;
      const langAux = localStorage.lang;
      const lang = langAux;
      const prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
      const langpatt = new RegExp("^en|es$");
      if (prjpatt.test(project) &&
                langpatt.test(lang)) {
        const url = `${BASE.url}doc/${lang}/project/${project}`;
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
      const projectAux = $stateParams.project;
      const project = projectAux;
      const filterAux = $scope.filter;
      const filter = filterAux;
      const finding = $scope.findingId;
      if (typeof project === "undefined" ||
                project === "") {
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
        if (projectData.length > 0 && projectData[0].proyecto_fluid.toLowerCase() === $scope.project.toLowerCase()) {
          $scope.view.project = true;
          $scope.loadFindingContent(projectData, vlang);
        }
        else {
          const reqProject = projectFtry.projectByName(project, filter);
          reqProject.then((response) => {
            $scope.view.project = true;
            if (!response.error) {
              // Tracking Mixpanel
              mixPanelDashboard.trackSearch("SearchFinding", userEmail, project);
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
        switch (datatest[cont].actor) {
        case "​Cualquier persona en Internet":
          datatest[cont].actor = $translate.instant("finding_formstack.actor.any_internet");
          break;
        case "Cualquier cliente de la organización":
          datatest[cont].actor = $translate.instant("finding_formstack.actor.any_costumer");
          break;
        case "Solo algunos clientes de la organización":
          datatest[cont].actor = $translate.instant("finding_formstack.actor.some_costumer");
          break;
        case "Cualquier persona con acceso a la estación":
          datatest[cont].actor = $translate.instant("finding_formstack.actor.any_access");
          break;
        case "Cualquier empleado de la organización":
          datatest[cont].actor = $translate.instant("finding_formstack.actor.any_employee");
          break;
        case "Solo algunos empleados":
          datatest[cont].actor = $translate.instant("finding_formstack.actor.some_employee");
          break;
        case "Solo un empleado":
          datatest[cont].actor = $translate.instant("finding_formstack.actor.one_employee");
          break;
        default:
          datatest[cont].actor = datatest[cont].actor;
        }
        switch (datatest[cont].autenticacion) {
        case "0.704 | Ninguna: No se requiere autenticación":
          datatest[cont].autenticacion = $translate.instant("finding_formstack.authentication.any_authen");
          break;
        case "0.560 | Única: Único punto de autenticación":
          datatest[cont].autenticacion = $translate.instant("finding_formstack.authentication.single_authen");
          break;
        case "0.450 | Multiple: Multiples puntos de autenticación":
          datatest[cont].autenticacion = $translate.instant("finding_formstack.authentication.multiple_authen");
          break;
        default:
          datatest[cont].autenticacion = datatest[cont].autenticacion;
        }
        switch (datatest[cont].categoria) {
        case "Actualizar y configurar las líneas base de seguridad de los componentes":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.update_base");
          break;
        case "Definir el modelo de autorización considerando el principio de mínimo privilegio":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.define_model");
          break;
        case "Desempeño":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.performance");
          break;
        case "Eventualidad":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.event");
          break;
        case "Evitar exponer la información técnica de la aplicación, servidores y plataformas":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.avoid_technical");
          break;
        case "Excluir datos sensibles del código fuente y del registro de eventos":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.exclude_datatest");
          break;
        case "Fortalecer controles en autenticación y manejo de sesión":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.strengt_authen");
          break;
        case "Fortalecer controles en el procesamiento de archivos":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.strengt_process");
          break;
        case "Fortalecer la protección de datos almacenados relacionados con contraseñas o llaves criptográficas":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.strengt_protect");
          break;
        case "Implementar controles para validar datos de entrada":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.validate_input");
          break;
        case "Mantenibilidad":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.maintain");
          break;
        case "Registrar eventos para trazabilidad y auditoría":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.record_event");
          break;
        case "Utilizar protocolos de comunicación seguros":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.secure_protoc");
          break;
        case "Validar la integridad de las transacciones en peticiones HTTP":
          datatest[cont].categoria = $translate.instant("finding_formstack.category.validate_http");
          break;
        default:
          datatest[cont].categoria = datatest[cont].categoria;
        }
        switch (datatest[cont].complejidadAcceso) {
        case "0.350 | Alto: Se requieren condiciones especiales como acceso administrativo":
          datatest[cont].complejidadAcceso = $translate.instant("finding_formstack.complexity.high_complex");
          break;
        case "0.610 | Medio: Se requieren algunas condiciones como acceso al sistema":
          datatest[cont].complejidadAcceso = $translate.instant("finding_formstack.complexity.medium_complex");
          break;
        case "0.710 | Bajo: No se requiere ninguna condición especial":
          datatest[cont].complejidadAcceso = $translate.instant("finding_formstack.complexity.low_complex");
          break;
        default:
          datatest[cont].complejidadAcceso = datatest[cont].complejidadAcceso;
        }
        switch (datatest[cont].escenario) {
        case "Anónimo desde Internet":
          datatest[cont].escenario = $translate.instant("finding_formstack.scenario.anon_inter");
          break;
        case "Anónimo desde Intranet":
          datatest[cont].escenario = $translate.instant("finding_formstack.scenario.anon_intra");
          break;
        case "Escaneo de Infraestructura":
          datatest[cont].escenario = $translate.instant("finding_formstack.scenario.infra_scan");
          break;
        case "Extranet usuario no autorizado":
          datatest[cont].escenario = $translate.instant("finding_formstack.scenario.unauth_extra");
          break;
        case "Internet usuario autorizado":
          datatest[cont].escenario = $translate.instant("finding_formstack.scenario.auth_inter");
          break;
        case "Internet usuario no autorizado":
          datatest[cont].escenario = $translate.instant("finding_formstack.scenario.unauth_inter");
          break;
        case "Intranet usuario autorizado":
          datatest[cont].escenario = $translate.instant("finding_formstack.scenario.auth_intra");
          break;
        case "Intranet usuario no autorizado":
          datatest[cont].escenario = $translate.instant("finding_formstack.scenario.unauth_inter");
          break;
        default:
          datatest[cont].escenario = datatest[cont].escenario;
        }
        switch (datatest[cont].estado) {
        case "Abierto":
          datatest[cont].estado = $translate.instant("finding_formstack.status.open");
          break;
        case "Cerrado":
          datatest[cont].estado = $translate.instant("finding_formstack.status.close");
          break;
        case "Parcialmente cerrado":
          datatest[cont].estado = $translate.instant("finding_formstack.status.part_close");
          break;
        default:
          datatest[cont].estado = datatest[cont].estado;
        }
        switch (datatest[cont].explotabilidad) {
        case "0.850 | Improbable: No existe un exploit":
          datatest[cont].explotabilidad = $translate.instant("finding_formstack.exploitability.improbable");
          break;
        case "0.900 | Conceptual: Existen pruebas de laboratorio":
          datatest[cont].explotabilidad = $translate.instant("finding_formstack.exploitability.conceptual");
          break;
        case "0.950 | Funcional: Existe exploit":
          datatest[cont].explotabilidad = $translate.instant("finding_formstack.exploitability.functional");
          break;
        case "1.000 | Alta: No se requiere exploit o se puede automatizar":
          datatest[cont].explotabilidad = $translate.instant("finding_formstack.exploitability.high");
          break;
        default:
          datatest[cont].explotabilidad = datatest[cont].explotabilidad;
        }
        switch (datatest[cont].explotable) {
        case "Si":
          datatest[cont].explotable = $translate.instant("finding_formstack.exploitable.yes");
          break;
        case "No":
          datatest[cont].explotable = $translate.instant("finding_formstack.exploitable.no");
          break;
        default:
          datatest[cont].explotable = datatest[cont].explotable;
        }
        switch (datatest[cont].impactoConfidencialidad) {
        case "0 | Ninguno: No se presenta ningún impacto":
          datatest[cont].impactoConfidencialidad = $translate.instant("finding_formstack.confidenciality.none");
          break;
        case "0.275 | Parcial: Se obtiene acceso a la información pero no control sobre ella":
          datatest[cont].impactoConfidencialidad = $translate.instant("finding_formstack.confidenciality.partial");
          break;
        case "0.660 | Completo: Se controla toda la información relacionada con el objetivo":
          datatest[cont].impactoConfidencialidad = $translate.instant("finding_formstack.confidenciality.complete");
          break;
        default:
          datatest[cont].impactoConfidencialidad = datatest[cont].impactoConfidencialidad;
        }
        switch (datatest[cont].impactoDisponibilidad) {
        case "0 | Ninguno: No se presenta ningún impacto":
          datatest[cont].impactoDisponibilidad = $translate.instant("finding_formstack.availability.none");
          break;
        case "0.275 | Parcial: Se presenta intermitencia en el acceso al objetivo":
          datatest[cont].impactoDisponibilidad = $translate.instant("finding_formstack.availability.partial");
          break;
        case "0.660 | Completo: Hay una caída total del objetivo":
          datatest[cont].impactoDisponibilidad = $translate.instant("finding_formstack.availability.complete");
          break;
        default:
          datatest[cont].impactoDisponibilidad = datatest[cont].impactoDisponibilidad;
        }
        switch (datatest[cont].impactoIntegridad) {
        case "0 | Ninguno: No se presenta ningún impacto":
          datatest[cont].impactoIntegridad = $translate.instant("finding_formstack.integrity.none");
          break;
        case "0.275 | Parcial: Es posible modificar cierta información del objetivo":
          datatest[cont].impactoIntegridad = $translate.instant("finding_formstack.integrity.partial");
          break;
        case "0.660 | Completo: Es posible modificar toda la información del objetivo":
          datatest[cont].impactoIntegridad = $translate.instant("finding_formstack.integrity.complete");
          break;
        default:
          datatest[cont].impactoIntegridad = datatest[cont].impactoIntegridad;
        }
        switch (datatest[cont].nivelConfianza) {
        case "0.900 | No confirmado: Existen pocas fuentes que reconocen la vulnerabilidad":
          datatest[cont].nivelConfianza = $translate.instant("finding_formstack.confidence.not_confirm");
          break;
        case "0.950 | No corroborado: La vulnerabilidad es reconocida por fuentes no oficiales":
          datatest[cont].nivelConfianza = $translate.instant("finding_formstack.confidence.not_corrob");
          break;
        case "1.000 | Confirmado: La vulnerabilidad es reconocida por el fabricante":
          datatest[cont].nivelConfianza = $translate.instant("finding_formstack.confidence.confirmed");
          break;
        default:
          datatest[cont].nivelConfianza = datatest[cont].nivelConfianza;
        }
        switch (datatest[cont].nivelResolucion) {
        case "0.950 | Paliativa: Existe un parche que no fue publicado por el fabricante":
          datatest[cont].nivelResolucion = $translate.instant("finding_formstack.resolution.palliative");
          break;
        case "0.870 | Oficial: Existe un parche disponible por el fabricante":
          datatest[cont].nivelResolucion = $translate.instant("finding_formstack.resolution.official");
          break;
        case "0.900 | Temporal: Existen soluciones temporales":
          datatest[cont].nivelResolucion = $translate.instant("finding_formstack.resolution.temporal");
          break;
        case "1.000 | Inexistente: No existe solución":
          datatest[cont].nivelResolucion = $translate.instant("finding_formstack.resolution.non_existent");
          break;
        default:
          datatest[cont].nivelResolucion = datatest[cont].nivelResolucion;
        }
        switch (datatest[cont].probabilidad) {
        case "100% Vulnerado Anteriormente":
          datatest[cont].probabilidad = $translate.instant("finding_formstack.probability.prev_vuln");
          break;
        case "75% Fácil de vulnerar":
          datatest[cont].probabilidad = $translate.instant("finding_formstack.probability.easy_vuln");
          break;
        case "50% Posible de vulnerar":
          datatest[cont].probabilidad = $translate.instant("finding_formstack.probability.possible_vuln");
          break;
        case "25% Difícil de vulnerar":
          datatest[cont].probabilidad = $translate.instant("finding_formstack.probability.diffic_vuln");
          break;
        default:
          datatest[cont].probabilidad = datatest[cont].probabilidad;
        }
        switch (datatest[cont].tipoHallazgoCliente) {
        case "Higiene":
          datatest[cont].tipoHallazgoCliente = $translate.instant("finding_formstack.findingType.hygiene");
          break;
        case "Vulnerabilidad":
          datatest[cont].tipoHallazgoCliente = $translate.instant("finding_formstack.findingType.vuln");
          break;
        default:
          datatest[cont].tipoHallazgoCliente = datatest[cont].tipoHallazgoCliente;
        }
        switch (datatest[cont].tipoPrueba) {
        case "Análisis":
          datatest[cont].tipoPrueba = $translate.instant("finding_formstack.test_method.analysis");
          break;
        case "Aplicación":
          datatest[cont].tipoPrueba = $translate.instant("finding_formstack.test_method.app");
          break;
        case "Binario":
          datatest[cont].tipoPrueba = $translate.instant("finding_formstack.test_method.binary");
          break;
        case "Código":
          datatest[cont].tipoPrueba = $translate.instant("finding_formstack.test_method.code");
          break;
        case "Infraestructura":
          datatest[cont].tipoPrueba = $translate.instant("finding_formstack.test_method.infras");
          break;
        default:
          datatest[cont].tipoPrueba = datatest[cont].tipoPrueba;
        }
        switch (datatest[cont].vectorAcceso) {
        case "0.646 | Red adyacente: Explotable desde el mismo segmento de red":
          datatest[cont].vectorAcceso = $translate.instant("finding_formstack.access_vector.adjacent");
          break;
        case "1.000 | Red: Explotable desde Internet":
          datatest[cont].vectorAcceso = $translate.instant("finding_formstack.access_vector.network");
          break;
        case "0.395 | Local: Explotable con acceso local al objetivo":
          datatest[cont].vectorAcceso = $translate.instant("finding_formstack.access_vector.local");
          break;
        default:
          datatest[cont].vectorAcceso = datatest[cont].vectorAcceso;
        }
        switch (datatest[cont].tratamiento) {
        case "Asumido":
          datatest[cont].tratamiento = $translate.instant("finding_formstack.treatment_header.asummed");
          break;
        case "Nuevo":
          datatest[cont].tratamiento = $translate.instant("finding_formstack.treatment_header.working");
          break;
        case "Remediar":
          datatest[cont].tratamiento = $translate.instant("finding_formstack.treatment_header.remediated");
          break;
        case "Resuelto":
          datatest[cont].tratamiento = $translate.instant("finding_formstack.treatment_header.resolved");
          break;
        default:
          datatest[cont].tratamiento = datatest[cont].tratamiento;
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
            data[cont].link = `${window.location.href.split("project/")[0]}project/${data[cont].proyecto_fluid.toLowerCase()}/${data[cont].id}/description`;
            if (typeof data[cont].registros !== "undefined" && data[cont].registros !== "") {
              data[cont].atributos = 1 + (data[cont].registros.match(/\n/g) || []).length;
            }
          }
          for (let cont = 0; cont < data.length - 1; cont++) {
            for (let incj = cont + 1; incj < data.length; incj++) {
              if (parseFloat(data[cont].criticidad) < parseFloat(data[incj].criticidad)) {
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
