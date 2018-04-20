/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,0.4,0.6,1,1.176,1.5,2,4,4.611,10,10.41,13,20,43.221,100,200,300,1000,3000] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, nonexploitLabel:true, totalHigLabel:true,
explotable:true, totalSegLabel:true, openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg, userName,
userEmail, Rollbar, aux:true, json:true, closeLabel:true, mixPanelDashboard, win:true, window, Organization, projectData:true, eventsData:true,
i:true, j:true
*/
/* eslint-env node*/
/**
 * @file ProjectCtrl.js
 * @author engineering@fluidattacks.com
 */
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
  "projectCtrl",
  function projectCtrl (
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
    $scope.search = function search () {
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
      const projectName = $scope.project;
      const filterAux = $scope.filter;
      const filter = filterAux;
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
        const reqProject = projectFtry.projectByName(projectName, filter);
        const reqEventualities = projectFtry.EventualityByName(projectName, "Name");
        reqProject.then((response) => {
          $scope.view.project = true;
          if (!response.error) {
            // Tracking Mixpanel
            mixPanelDashboard.trackSearch("SearchFinding", userEmail, projectName);
            if (response.data.length === 0) {
              $scope.view.project = false;
              $scope.view.finding = false;
              $msg.error($translate.instant("proj_alerts.not_found"));
            }
            else {
              $scope.data = response.data;
              projectData = response.data;
              const org = Organization.toUpperCase();
              const projt = $stateParams.project.toUpperCase();
              $scope.alertHeader(org, projt);
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
        reqEventualities.then((response) => {
          if (!response.error) {
            eventsData = response.data;
            mixPanelDashboard.trackSearch("SearchEventuality", userEmail, projectName);
            $("#search_section").show();
            $("[data-toggle=\"tooltip\"]").tooltip();
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
      return true;
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
