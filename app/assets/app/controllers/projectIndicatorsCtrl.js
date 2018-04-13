/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,0.4,0.6,1,1.176,1.5,2,4,4.611,10,10.41,13,20,43.221,100,200,300,1000,3000] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, nonexploitLabel:true, total_higLabel:true,
explotable:true, total_segLabel:true, openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg, userName,
userEmail, Rollbar, aux:true, json:true, closeLabel:true, mixPanelDashboard, win:true, window, Organization, projectData:true, eventsData:true,
i:true, j:true
*/
/* eslint-env node*/
/**
 * @file ProjectCtrl.js
 * @author engineering@fluidattacks.com
 */
/* Table Formatter */

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
  "projectIndicatorsCtrl",
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
        $(".equalWidgetHeight").matchHeight();
        mixPanelDashboard.trackReports("ProjectIndicators", userName, userEmail, org, projt);
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
    $scope.calculateCardinality = function (data) {
      let total_severity = 0;
      let cardinalidad = 0;
      let cardinalidad_total = 0;
      data.data.forEach(function (cont) {
        cardinalidad += parseInt(cont.cardinalidad, 10);
        cardinalidad_total += parseInt(cont.cardinalidad_total, 10);
      });
      $scope.metricsList = [];
      $scope.metricsList.push({
        "color": "background-color: #2197d6;",
        "description": $translate.instant("search_findings.filter_labels.findings"),
        "icon": "s7-id",
        "value": data.data.length
      });
      $scope.metricsList.push({
        "color": "background-color: #aa2d30;",
        "description": $translate.instant("search_findings.filter_labels.cardinalities"),
        "icon": "s7-unlock",
        "value": cardinalidad
      });
      let severity = 0;
      data.data.forEach(function (cont) {
        try {
          if (cont.tipo_hallazgo === "Seguridad") {
            const ImpCon = parseFloat(cont.impacto_confidencialidad.split(" | ")[0]);
            const ImpInt = parseFloat(cont.impacto_integridad.split(" | ")[0]);
            const ImpDis = parseFloat(cont.impacto_disponibilidad.split(" | ")[0]);
            const AccCom = parseFloat(cont.complejidad_acceso.split(" | ")[0]);
            const AccVec = parseFloat(cont.vector_acceso.split(" | ")[0]);
            const Auth = parseFloat(cont.autenticacion.split(" | ")[0]);
            const Explo = parseFloat(cont.explotabilidad.split(" | ")[0]);
            const Resol = parseFloat(cont.nivel_resolucion.split(" | ")[0]);
            const Confi = parseFloat(cont.nivel_confianza.split(" | ")[0]);
            const BaseScore = ((0.6 * (10.41 * (1 - ((1 - ImpCon) * (1 - ImpInt) * (1 - ImpDis))))) + (0.4 * (20 * AccCom * Auth * AccVec)) - 1.5) * 1.176;
            severity += BaseScore * parseFloat(cont.cardinalidad_total);
          }
        }
        catch (err) {
          Rollbar.error("Error: An error ocurred calculating cardinality", err);
        }
      });
      const req = projectFtry.TotalSeverity($scope.project.toLowerCase());
      req.then(function (response) {
        if (!response.error) {
          if (response.data.length > 0) {
            for (let cont = 0; cont < response.data.length; cont++) {
              const target = (parseInt(response.data[cont].lines, 10) / 1000) + (parseInt(response.data[cont].fields, 10) / 4);
              total_severity = severity / ((4.611 * target) + 43.221) * 100;
              $scope.metricsList.push({
                "color": "background-color: #ef4c43;",
                "description": $translate.instant("search_findings.filter_labels.criticity"),
                "icon": "s7-graph1",
                "value": "n%".replace("n", total_severity.toFixed(0))
              });
              $scope.metricsList.push({
                "color": "background-color: #00cb77;",
                "description": $translate.instant("search_findings.filter_labels.closure"),
                "icon": "s7-like2",
                "value": "n%".replace("n", Math.round((1 - (cardinalidad / cardinalidad_total)) * 100).toString())
              });
            }
          }
          else {
            total_severity = severity;
            $scope.metricsList.push({
              "color": "background-color: #ef4c43;",
              "description": $translate.instant("search_findings.filter_labels.criticity"),
              "icon": "s7-graph1",
              "value": total_severity.toFixed(0)
            });
            $scope.metricsList.push({
              "color": "background-color: #00cb77;",
              "description": $translate.instant("search_findings.filter_labels.closure"),
              "icon": "s7-like2",
              "value": "n%".replace("n", Math.round((1 - (cardinalidad / cardinalidad_total)) * 100).toString())
            });
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
    $scope.mainGraphtypePieChart = function () {
      const currData = $scope.data;
      let total_seg = 0;
      let total_hig = 0;
      currData.forEach(function (val, cont) {
        const tipo = val.tipo_hallazgo;
        if (val.estado !== "Cerrado" && val.estado !== "Closed") {
          if (tipo === "Seguridad") {
            total_seg += 1;
          }
          else {
            total_hig += 1;
          }
        }
      });
      const seg_transl = $translate.instant("grapType.seg_label");
      const hig_transl = $translate.instant("grapType.hig_label");
      const total_segLabel = seg_transl + " :n%".replace(":n", (total_seg * 100 / (total_seg + total_hig)).toFixed(2).toString());
      const total_higLabel = hig_transl + " :n%".replace(":n", (total_hig * 100 / (total_seg + total_hig)).toFixed(2).toString());
      $("#grapType").empty();
      Morris.Donut({
        "data": [
          {
            "color": "#ff1a1a",
            "label": total_segLabel,
            "value": total_seg
          },
          {
            "color": "#31c0be",
            "label": total_higLabel,
            "value": total_hig
          }
        ],
        "element": "grapType",
        "resize": true
      });
    };
    $scope.mainGraphexploitPieChart = function () {
      const currData = $scope.data;
      let exploit = 0;
      let nonexploit = 0;
      currData.forEach(function (val, cont) {
        const explotable = val.explotabilidad;
        if (val.estado !== "Cerrado" && val.estado !== "Closed") {
          if (explotable === "1.000 | Alta: No se requiere exploit o se puede automatizar" || explotable === "0.950 | Funcional: Existe exploit" || explotable === "1.000 | High: Exploit is not required or it can be automated" || explotable === "0.950 | Functional: There is an exploit") {
            exploit += 1;
          }
          else {
            nonexploit += 1;
          }
        }
      });
      const exploit_transl = $translate.instant("grapExploit.exploit_label");
      const nonexploit_transl = $translate.instant("grapExploit.nonexploit_label");
      const exploitLabel = exploit_transl + " :n%".replace(":n", (exploit * 100 / (exploit + nonexploit)).toFixed(2).toString());
      const nonexploitLabel = nonexploit_transl + " :n%".replace(":n", (nonexploit * 100 / (exploit + nonexploit)).toFixed(2).toString());
      $("#grapExploit").empty();
      Morris.Donut({
        "data": [
          {
            "color": "#ff1a1a",
            "label": exploitLabel,
            "value": exploit
          },
          {
            "color": "#31c0be",
            "label": nonexploitLabel,
            "value": nonexploit
          }
        ],
        "element": "grapExploit",
        "resize": true
      });
    };
    $scope.mainGraphstatusPieChart = function () {
      const currData = $scope.data;
      let total = 0;
      let open = 0;
      let partial = 0;
      let close = 0;
      currData.forEach(function (val, cont) {
        const estado = val.estado;
        total += 1;
        if (estado === "Abierto" || estado === "Open") {
          open += 1;
        }
        else if (estado === "Cerrado" || estado === "Closed") {
          close += 1;
        }
        else {
          partial += 1;
        }
      });
      total = parseFloat(total);
      const open_transl = $translate.instant("grapStatus.open_label");
      const partial_transl = $translate.instant("grapStatus.partial_label");
      const close_transl = $translate.instant("grapStatus.close_label");
      const openLabel = open_transl + " :n%".replace(":n", (open * 100 / total).toFixed(2).toString());
      const partialLabel = partial_transl + " :n%".replace(":n", (partial * 100 / total).toFixed(2).toString());
      const closeLabel = close_transl + " :n%".replace(":n", (close * 100 / total).toFixed(2).toString());
      $("#grapStatus").empty();
      Morris.Donut({
        "data": [
          {
            "color": "#ff1a1a",
            "label": openLabel,
            "value": open
          },
          {
            "color": "#ffbf00",
            "label": partialLabel,
            "value": partial
          },
          {
            "color": "#31c0be",
            "label": closeLabel,
            "value": close
          }
        ],
        "element": "grapStatus",
        "resize": true
      });
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
        if (projectData.length > 0 && projectData[0].proyecto_fluid.toLowerCase() === $scope.project.toLowerCase()) {
          $scope.view.project = true;
          $scope.loadIndicatorsContent(projectData);
        }
        else {
          const reqProject = projectFtry.projectByName(project, filter);
          reqProject.then(function (response) {
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
                $scope.loadIndicatorsContent(projectData);
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
    };
    $scope.loadIndicatorsContent = function (datatest) {
      const org = Organization.toUpperCase();
      const projt = $stateParams.project.toUpperCase();
      $scope.alertHeader(org, projt);
      $scope.calculateCardinality({"data": datatest});
      $timeout($scope.mainGraphexploitPieChart, 200);
      $timeout($scope.mainGraphtypePieChart, 200);
      $timeout($scope.mainGraphstatusPieChart, 200);
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
    $scope.urlIndicators = function () {
      $state.go("ProjectIndicators", {"project": $scope.project});
    };
    $scope.urlFindings = function () {
      $state.go("ProjectFindings", {"project": $scope.project});
    };
    $scope.urlEvents = function () {
      $state.go("ProjectEvents", {"project": $scope.project});
    };
    $scope.init();
  }
);
