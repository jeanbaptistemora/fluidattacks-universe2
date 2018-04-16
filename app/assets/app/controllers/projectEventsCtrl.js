/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,0.4,0.6,1,1.176,1.5,2,4,4.611,10,10.41,13,20,43.221,100,200,300,1000,3000] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, nonexploitLabel:true, totalHigLabel:true,
explotable:true, totalSegLabel:true, openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg, userName,
userEmail, Rollbar, aux:true, json:true, closeLabel:true, mixPanelDashboard, win:true, window, Organization, projectData:true, eventsData:true,
i:true, j:true
*/
/* eslint-env node*/
/**
 * @file projectEventsCtrl.js
 * @author engineering@fluidattacks.com
 */

/**
 * Function labelEventState return html code for specific label
 */
function labelEventState (value, row, index) {
  if (value === "Tratada") {
    return "<label class='label label-success' style='background-color: #31c0be'>Tratada</label>";
  }
  else if (value === "Solved") {
    return "<label class='label label-success' style='background-color: #31c0be'>Solved</label>";
  }
  else if (value === "Pendiente") {
    return "<label class='label label-danger' style='background-color: #f22;'>Pendiente</label>";
  }
  else if (value === "Unsolved") {
    return "<label class='label label-danger' style='background-color: #f22;'>Unsolved</label>";
  }
}

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
  function projectEventsCtrl (
    $scope, $location,
    $uibModal, $timeout,
    $state, $stateParams,
    $translate, projectFtry
  ) {
    $scope.init = function init () {
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
    $scope.goUp = function goUp () {
      $("html, body").animate({"scrollTop": 0}, "fast");
    };
    $scope.alertHeader = function alertHeader (company, project) {
      const req = projectFtry.getAlerts(company, project);
      req.then(function setalertHeader (response) {
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
    $scope.search = function search () {
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
        if (eventsData.length > 0 && eventsData[0].proyecto_fluid.toLowerCase() === $scope.project.toLowerCase()) {
          $scope.view.project = true;
          $scope.loadEventContent(eventsData, vlang, project);
        }
        else {
          const reqEventualities = projectFtry.EventualityByName(project, "Name");
          reqEventualities.then(function resEventualityByName (response) {
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
    $scope.urlIndicators = function urlIndicators () {
      $state.go("ProjectIndicators", {"project": $scope.project});
    };
    $scope.urlFindings = function urlFindings () {
      $state.go("ProjectFindings", {"project": $scope.project});
    };
    $scope.urlEvents = function urlEvents () {
      $state.go("ProjectEvents", {"project": $scope.project});
    };
    $scope.loadEventContent = function loadEventContent (data, vlang, project) {
      const org = Organization.toUpperCase();
      const projt = project.toUpperCase();
      $scope.alertHeader(org, projt);
      for (let cont = 0; cont < data.length; cont++) {
        switch (data[cont].tipo) {
        case "Autorización para ataque especial":
          data[cont].tipo = $translate.instant("eventFormstack.type.auth_attack");
          break;
        case "Alcance difiere a lo aprobado":
          data[cont].tipo = $translate.instant("eventFormstack.type.toe_differs");
          break;
        case "Aprobación de alta disponibilidad":
          data[cont].tipo = $translate.instant("eventFormstack.type.high_approval");
          break;
        case "Insumos incorrectos o faltantes":
          data[cont].tipo = $translate.instant("eventFormstack.type.incor_supplies");
          break;
        case "Cliente suspende explicitamente":
          data[cont].tipo = $translate.instant("eventFormstack.type.explic_suspend");
          break;
        case "Cliente aprueba cambio de alcance":
          data[cont].tipo = $translate.instant("eventFormstack.type.approv_change");
          break;
        case "Cliente cancela el proyecto/hito":
          data[cont].tipo = $translate.instant("eventFormstack.type.cancel_proj");
          break;
        case "Cliente detecta ataque":
          data[cont].tipo = $translate.instant("eventFormstack.type.det_attack");
          break;
        case "Otro":
          data[cont].tipo = $translate.instant("eventFormstack.type.other");
          break;
        case "Ambiente no accesible":
          data[cont].tipo = $translate.instant("eventFormstack.type.inacc_ambient");
          break;
        case "Ambiente inestable":
          data[cont].tipo = $translate.instant("eventFormstack.type.uns_ambient");
          break;
        default:
          data[cont].tipo = data[cont].tipo;
        }
        switch (data[cont].estado) {
        case "Pendiente":
          data[cont].estado = $translate.instant("eventFormstack.status.unsolve");
          break;
        case "Tratada":
          data[cont].estado = $translate.instant("eventFormstack.status.solve");
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
              $scope.close = function close () {
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
