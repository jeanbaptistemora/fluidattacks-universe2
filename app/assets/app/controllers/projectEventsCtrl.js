/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,0.4,0.6,1,1.176,1.5,2,4,4.611,10,10.41,13,20,43.221,100,200,300,1000,3000] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, nonexploitLabel:true, total_higLabel:true,
explotable:true, total_segLabel:true, openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg, userName,
userEmail, Rollbar, aux:true, json:true, closeLabel:true, mixPanelDashboard, win:true, window, Organization, projectData:true, eventsData:true,
i:true, j:true
*/
/* eslint-env node*/
/**
 * @file projectEventsCtrl.js
 * @author engineering@fluidattacks.com
 */

/**
 * Controlador de vista de proyectos
 * @name projectEventsCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @return {undefined}
 */
/** @export */
integrates.controller(
  "projectEventsCtrl",
  function (
    $scope, $location,
    $uibModal, $timeout,
    $state, $stateParams,
    $translate, projectFtry
  ) {
    $scope.init = function () {
      const project = $stateParams.project;
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
        mixPanelDashboard.trackReports("ProjectEvents", userName, userEmail, org, projt);
      }
      // Asigna el evento buscar al textbox search y tecla enter
      $scope.configKeyboardView();
      $scope.goUp();
      $scope.finding = {};
    };
    $scope.goUp = function () {
      $("html, body").animate({"scrollTop": 0}, "fast");
    };
    $scope.alertHeader = function (company, project) {
      const req = projectFtry.getAlerts(company, project);
      req.then(function (response) {
        if (!response.error && response.data.length > 0) {
          if (response.data.status_act === "1") {
            let html = "<div class=\"alert alert-danger-2\">";
            html += `<strong>Atención! </strong>${response.data[0].message}</div>`;
            document.getElementById("header_alert").innerHTML = html;
          }
        }
      });
    };
    $scope.configKeyboardView = function () {
      document.onkeypress = function (ev) {
        // Buscar un proyecto
        if (ev.keyCode === 13) {
          if ($("#project").is(":focus")) {
            $scope.search();
          }
        }
      };
    };
    $scope.search = function () {
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
      const project = $scope.project;
      const filter = $scope.filter;
      const finding = $scope.findingId;
      if (typeof project === "undefined" ||
                project === "") {
        const attention_at = $translate.instant("proj_alerts.attent_title");
        const attention_ac = $translate.instant("proj_alerts.attent_cont");
        $msg.warning(attention_ac, attention_at);
        return false;
      }
      if ($stateParams.project !== $scope.project) {
        $state.go("ProjectIndicators", {"project": $scope.project});
      }
      else if ($stateParams.project === $scope.project) {
        $scope.view.project = false;
        $scope.view.finding = false;

        /* Handling presentation button */
        const search_at = $translate.instant("proj_alerts.search_title");
        const search_ac = $translate.instant("proj_alerts.search_cont");
        $msg.info(search_ac, search_at);
        if (eventsData.length > 0 && eventsData[0].proyecto_fluid.toLowerCase() === $scope.project.toLowerCase()) {
          $scope.view.project = true;
          $scope.loadEventContent(eventsData, vlang, project);
        }
        else {
          const reqEventualities = projectFtry.EventualityByName(project, "Name");
          reqEventualities.then(function (response) {
            if (!response.error) {
              $scope.view.project = true;
              eventsData = response.data;
              $scope.loadEventContent(eventsData, vlang, project);
            }
            else if (response.message === "Access to project denied") {
              Rollbar.warning("Warning: Access to event denied");
              $msg.error($translate.instant("proj_alerts.access_denied"));
            }
            else {
              Rollbar.warning("Warning: Event not found");
              $msg.error($translate.instant("proj_alerts.not_found"));
            }
          });
        }
      }
    };
    $scope.urlIndicators = function () {
      $state.go("ProjectIndicators", {"project": $scope.project});
    };
    $scope.urlFindings = function () {
      $state.go("ProjectFindings", {"project": $scope.project});
    };
    $scope.urlEvents = function () {
      $state.go("ProjectEvents", {"project": $scope.project});
    };
    $scope.loadEventContent = function (data, vlang, project) {
      const org = Organization.toUpperCase();
      const projt = project.toUpperCase();
      $scope.alertHeader(org, projt);
      for (let cont = 0; cont < data.length; cont++) {
        switch (data[cont].tipo) {
        case "Autorización para ataque especial":
          data[cont].tipo = $translate.instant("event_formstack.type.auth_attack");
          break;
        case "Alcance difiere a lo aprobado":
          data[cont].tipo = $translate.instant("event_formstack.type.toe_differs");
          break;
        case "Aprobación de alta disponibilidad":
          data[cont].tipo = $translate.instant("event_formstack.type.high_approval");
          break;
        case "Insumos incorrectos o faltantes":
          data[cont].tipo = $translate.instant("event_formstack.type.incor_supplies");
          break;
        case "Cliente suspende explicitamente":
          data[cont].tipo = $translate.instant("event_formstack.type.explic_suspend");
          break;
        case "Cliente aprueba cambio de alcance":
          data[cont].tipo = $translate.instant("event_formstack.type.approv_change");
          break;
        case "Cliente cancela el proyecto/hito":
          data[cont].tipo = $translate.instant("event_formstack.type.cancel_proj");
          break;
        case "Cliente detecta ataque":
          data[cont].tipo = $translate.instant("event_formstack.type.det_attack");
          break;
        case "Otro":
          data[cont].tipo = $translate.instant("event_formstack.type.other");
          break;
        case "Ambiente no accesible":
          data[cont].tipo = $translate.instant("event_formstack.type.inacc_ambient");
          break;
        case "Ambiente inestable":
          data[cont].tipo = $translate.instant("event_formstack.type.uns_ambient");
          break;
        default:
          data[cont].tipo = data[cont].tipo;
        }
        switch (data[cont].estado) {
        case "Pendiente":
          data[cont].estado = $translate.instant("event_formstack.status.unsolve");
          break;
        case "Tratada":
          data[cont].estado = $translate.instant("event_formstack.status.solve");
          break;
        default:
          data[cont].estado = data[cont].estado;
        }
      }
      mixPanelDashboard.trackSearch("SearchEventuality", userEmail, project);
      // CONFIGURACION DE TABLA
      $("#tblEventualities").bootstrapTable("destroy");
      $("#tblEventualities").bootstrapTable({
        data,
        "locale": vlang,
        "onClickRow" (row) {
          const modalInstance = $uibModal.open({
            "animation": true,
            "backdrop": "static",
            "controller" ($scope, $uibModalInstance, evt) {
              $scope.evt = evt;
              // Tracking mixpanel
              const org = Organization.toUpperCase();
              const projt = project.toUpperCase();
              mixPanelDashboard.trackReadEventuality(userName, userEmail, org, projt, evt.id);
              $scope.close = function () {
                $uibModalInstance.close();
              };
            },
            "resolve": {"evt": row},
            "templateUrl": `${BASE.url}assets/views/project/eventualityMdl.html`
          });
        }
      });
      $("#tblEventualities").bootstrapTable("refresh");
      // MANEJO DEL UI
      $("#search_section").show();
      $("[data-toggle=\"tooltip\"]").tooltip();
    };
    $scope.init();
  }
);
