/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,0.4,0.6,1,1.176,
                            1.5,2,4,4.611,10,10.41,13,20,43.221,100,200,
                            300,1000,3000] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, i:true, j:true,
nonexploitLabel:true, totalHigLabel:true, explotable:true, totalSegLabel:true,
openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg,
userName, userEmail, Rollbar, aux:true, json:true, closeLabel:true,
mixPanelDashboard, win:true, Organization, projectData:true, eventsData:true
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
  function projectIndicatorsCtrl (
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
        $(".equalWidgetHeight").matchHeight();
        mixPanelDashboard.trackReports(
          "ProjectIndicators",
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
            html += "<strong>Atención! " +
                    `</strong>${response.data[0].message}</div>`;
            document.getElementById("header_alert").innerHTML = html;
          }
        }
      });
    };
    $scope.calculateCardinality = function calculateCardinality (data) {
      let totalSeverity = 0;
      let cardinalidad = 0;
      let cardinalidadTotal = 0;
      let maximumSeverity = 0;
      let oldestFinding = 0;
      let openEvents = 0;
      data.data.forEach((cont) => {
        cardinalidad += parseInt(cont.cardinalidad, 10);
        cardinalidadTotal += parseInt(cont.cardinalidad_total, 10);
        if (maximumSeverity < cont.criticidad) {
          maximumSeverity = cont.criticidad;
        }
        if (oldestFinding < cont.edad) {
          oldestFinding = cont.edad;
        }
      });
      for (let event = 0; event < eventsData.length; event++) {
        if (eventsData[event].estado === "Unsolved" ||
              eventsData[event].estado === "Pendiente") {
          openEvents += 1;
        }
      }
      $scope.metricsList = [];
      $scope.metricsList.push({
        "color": "background-color: #2197d6;",
        "description": $translate.instant("search_findings." +
                                          "filter_labels.findings"),
        "icon": "s7-id",
        "value": data.data.length
      });
      $scope.metricsList.push({
        "color": "background-color: #ff9930;",
        "description": $translate.instant("search_findings." +
                                          "filter_labels.vulnerabilities"),
        "icon": "s7-info",
        "value": cardinalidadTotal
      });
      $scope.metricsList.push({
        "color": "background-color: #aa2d30;",
        "description": $translate.instant("search_findings." +
                                          "filter_labels.cardinalities"),
        "icon": "s7-attention",
        "value": cardinalidad
      });
      $scope.metricsList.push({
        "color": "background-color: #2e4050;",
        "description": $translate.instant("search_findings." +
                                          "filter_labels.maximumSeverity"),
        "icon": "s7-gleam",
        "value": maximumSeverity
      });
      $scope.metricsList.push({
        "color": "background-color: #9f5ab1;",
        "description": $translate.instant("search_findings." +
                                          "filter_labels.oldestFinding"),
        "icon": "s7-date",
        "value": oldestFinding
      });
      $scope.metricsList.push({
        "color": "background-color: #0a40ae;",
        "description": $translate.instant("search_findings." +
                                          "filter_labels.openEvents"),
        "icon": "s7-way",
        "value": openEvents
      });
      let severity = 0;
      data.data.forEach((cont) => {
        try {
          if (cont.tipo_hallazgo === "Seguridad") {
            const ImpCon =
                      parseFloat(cont.impactoConfidencialidad.split(" | ")[0]);
            const ImpInt =
                      parseFloat(cont.impactoIntegridad.split(" | ")[0]);
            const ImpDis =
                      parseFloat(cont.impactoDisponibilidad.split(" | ")[0]);
            const AccCom = parseFloat(cont.complejidadAcceso.split(" | ")[0]);
            const AccVec = parseFloat(cont.vectorAcceso.split(" | ")[0]);
            const Auth = parseFloat(cont.autenticacion.split(" | ")[0]);
            const Explo = parseFloat(cont.explotabilidad.split(" | ")[0]);
            const Resol = parseFloat(cont.nivelResolucion.split(" | ")[0]);
            const Confi = parseFloat(cont.nivelConfianza.split(" | ")[0]);
            const BaseScore = ((0.6 * (10.41 * (1 - ((1 - ImpCon) *
                              (1 - ImpInt) * (1 - ImpDis))))) +
                              (0.4 * (20 * AccCom * Auth * AccVec)) - 1.5) *
                              1.176;
            severity += BaseScore * parseFloat(cont.cardinalidad_total);
          }
        }
        catch (err) {
          Rollbar.error("Error: An error ocurred calculating cardinality", err);
        }
      });
      const req = projectFtry.TotalSeverity($scope.project.toLowerCase());
      req.then((response) => {
        if (!response.error) {
          if (response.data.length > 0) {
            for (let cont = 0; cont < response.data.length; cont++) {
              const target = (parseInt(response.data[cont].lines, 10) / 1000) +
                             (parseInt(response.data[cont].fields, 10) / 4);
              totalSeverity = severity / ((4.611 * target) + 43.221) * 100;
              $scope.metricsList.push({
                "color": "background-color: #ef4c43;",
                "description": $translate.instant("search_findings." +
                                                  "filter_labels.criticity"),
                "icon": "s7-graph1",
                "value": "n%".replace("n", totalSeverity.toFixed(0))
              });
              $scope.metricsList.push({
                "color": "background-color: #00cb77;",
                "description": $translate.instant("search_findings." +
                                                  "filter_labels.closure"),
                "icon": "s7-like2",
                "value": "n%".replace("n", Math.round((1 - (cardinalidad /
                                                       cardinalidadTotal)) *
                                                       100).toString())
              });
            }
          }
          else {
            totalSeverity = severity;
            $scope.metricsList.push({
              "color": "background-color: #ef4c43;",
              "description": $translate.instant("search_findings." +
                                                "filter_labels.criticity"),
              "icon": "s7-graph1",
              "value": totalSeverity.toFixed(0)
            });
            $scope.metricsList.push({
              "color": "background-color: #00cb77;",
              "description": $translate.instant("search_findings." +
                                                "filter_labels.closure"),
              "icon": "s7-like2",
              "value": "n%".replace("n", Math.round((1 - (cardinalidad /
                                                     cardinalidadTotal)) *
                                                     100).toString())
            });
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
    $scope.mainGraphtypePieChart = function mainGraphtypePieChart () {
      const currData = $scope.data;
      let totalSeg = 0;
      let totalHig = 0;
      currData.forEach((val, cont) => {
        const tipo = val.tipo_hallazgo;
        if (val.estado !== "Cerrado" && val.estado !== "Closed") {
          if (tipo === "Seguridad") {
            totalSeg += 1;
          }
          else {
            totalHig += 1;
          }
        }
      });
      const segTransl = $translate.instant("grapType.seg_label");
      const higTransl = $translate.instant("grapType.hig_label");
      const totalSegLabel = segTransl + " :n%".replace(":n", (totalSeg * 100 /
                            (totalSeg + totalHig)).toFixed(2).toString());
      const totalHigLabel = higTransl + " :n%".replace(":n", (totalHig * 100 /
                            (totalSeg + totalHig)).toFixed(2).toString());
      $("#grapType").empty();
      Morris.Donut({
        "data": [
          {
            "color": "#ff1a1a",
            "label": totalSegLabel,
            "value": totalSeg
          },
          {
            "color": "#31c0be",
            "label": totalHigLabel,
            "value": totalHig
          }
        ],
        "element": "grapType",
        "resize": true
      });
    };
    $scope.mainGraphexploitPieChart = function mainGraphexploitPieChart () {
      const currData = $scope.data;
      let exploit = 0;
      let nonexploit = 0;
      currData.forEach((val, cont) => {
        const explotable = val.explotabilidad;
        if (val.estado !== "Cerrado" && val.estado !== "Closed") {
          if (explotable === "1.000 | Alta: No se requiere exploit o se puede" +
                             " automatizar" || explotable === "0.950 | " +
                             "Funcional: Existe exploit" || explotable ===
                             "1.000 | High: Exploit is not required or it can" +
                             " be automated" || explotable === "0.950 | " +
                             "Functional: There is an exploit") {
            exploit += 1;
          }
          else {
            nonexploit += 1;
          }
        }
      });
      const exploitTransl = $translate.instant("grapExploit.exploit_label");
      const nonExploitTransl = $translate.instant("grapExploit." +
                                                  "nonexploit_label");
      const exploitLabel = exploitTransl + " :n%".replace(":n", (exploit *
                           100 / (exploit + nonexploit)).toFixed(2).toString());
      const nonexploitLabel = nonExploitTransl + " :n%".replace(
        ":n",
        (nonexploit * 100 / (exploit +
                              nonexploit)).toFixed(2).toString()
      );
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
    $scope.mainGraphstatusPieChart = function mainGraphstatusPieChart () {
      const currData = $scope.data;
      let total = 0;
      let open = 0;
      let partial = 0;
      let close = 0;
      currData.forEach((val, cont) => {
        const findingStatus = val.estado;
        total += 1;
        if (findingStatus === "Abierto" || findingStatus === "Open") {
          open += 1;
        }
        else if (findingStatus === "Cerrado" || findingStatus === "Closed") {
          close += 1;
        }
        else {
          partial += 1;
        }
      });
      total = parseFloat(total);
      const openTransl = $translate.instant("grapStatus.open_label");
      const partialTransl = $translate.instant("grapStatus.partial_label");
      const closeTransl = $translate.instant("grapStatus.close_label");
      const openLabel = openTransl + " :n%".replace(":n", (open * 100 /
                        total).toFixed(2).toString());
      const partialLabel = partialTransl + " :n%".replace(":n", (partial * 100 /
                           total).toFixed(2).toString());
      const closeLabel = closeTransl + " :n%".replace(":n", (close * 100 /
                         total).toFixed(2).toString());
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
    $scope.search = function search () {
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
      const projectName = $scope.project;
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
        if (eventsData.length === 0 || (eventsData.length > 0 &&
                   eventsData[0].proyecto_fluid.toLowerCase() !==
                   $scope.project.toLowerCase())) {
          const reqEventualities = projectFtry.EventualityByName(
            projectName,
            "Name"
          );
          reqEventualities.then((response) => {
            if (!response.error) {
              eventsData = response.data;
            }
            else if (response.message === "Access to project denied") {
              Rollbar.warning("Warning: Access to event denied");
              $msg.error($translate.instant("proj_alerts.access_denied"));
            }
            else {
              Rollbar.warning("Warning: Event not found");
              $msg.error($translate.instant("proj_alerts.eventExist"));
            }
          });
        }
        if (projectData.length > 0 &&
            projectData[0].proyecto_fluid.toLowerCase() ===
            $scope.project.toLowerCase()) {
          $scope.view.project = true;
          $scope.loadIndicatorsContent(projectData);
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
      return true;
    };
    $scope.loadIndicatorsContent = function loadIndicatorsContent (datatest) {
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
