/* eslint-disable max-lines */
/* eslint no-magic-numbers: ["error", { "ignore":[-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow":
                                   ["$scope","$stateParams", "projectFtry"] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, projectData:true,
nonexploitLabel:true, totalHigLabel:true, $scope:true,explotable:true, i:true,
totalSegLabel:true, openLabel:true, partialLabel:true, $msg, integrates, j:true,
document, userName, userEmail, Rollbar, aux:true, json:true, eventsData:true, $,
closeLabel:true, mixPanelDashboard, win:true, window, Organization, userRole,
fieldsToTranslate, keysToTranslate, removeHour:true, labelState:true
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
removeHour = function removeHour (value) {
  if (value.indexOf(":") !== -1) {
    return value.split(" ")[0];
  }
  return value;
};

/**
 * @function labelState
 * @param {string} value Status of the finding
 * @member integrates.registerCtrl
 * @return {string} Html code for specific label
 */
labelState = function labelState (value) {
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
};

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
    $state, $stateParams, $translate,
    projectFtry, functionsFtry1, functionsFtry3
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
      functionsFtry3.configKeyboardView($scope);
      $scope.goUp();
      $scope.finding = {};
    };
    $scope.goUp = function goUp () {
      $("html, body").animate({"scrollTop": 0}, "fast");
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
        if (eventsData.length === 0 || (eventsData.length > 0 &&
                   eventsData[0].proyecto_fluid.toLowerCase() !==
                   $scope.project.toLowerCase())) {
          const reqEventualities = projectFtry.eventualityByName(
            projectName,
            "Name"
          );
          reqEventualities.then((response) => {
            if (!response.error) {
              if (typeof response.data === "undefined") {
                location.reload();
              }
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
              if (typeof response.data === "undefined") {
                location.reload();
              }
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
      functionsFtry1.alertHeader(org, projt);
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
      if (!$scope.isManager) {
        $scope.openEvents = projectFtry.alertEvents(eventsData);
        $scope.atAlert = $translate.instant("main_content.eventualities." +
                                            "descSingularAlert1");
        if ($scope.openEvents === 1) {
          $scope.descAlert1 = $translate.instant("main_content.eventualities." +
                                                  "descSingularAlert2");
          $scope.descAlert2 = $translate.instant("main_content.eventualities." +
                                                  "descSingularAlert3");
          $("#events_alert").show();
        }
        else if ($scope.openEvents > 1) {
          $scope.descAlert1 = $translate.instant("main_content.eventualities." +
                                                  "descPluralAlert1");
          $scope.descAlert2 = $translate.instant("main_content.eventualities." +
                                                  "descPluralAlert2");
          $("#events_alert").show();
        }
      }
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
          let severity = 0;
          data.forEach((cont) => {
            try {
              if (cont.tipo_hallazgo === "Seguridad") {
                const BaseScore = projectFtry.calCCssv2(cont)[0];
                severity += BaseScore * parseFloat(cont.cardinalidad_total);
              }
            }
            catch (err) {
              Rollbar.error("Error: An error ocurred calculating " +
                            "cardinality", err);
            }
          });
          $scope.totalSeverity = severity.toFixed(0);
          $scope.closeModalAvance = function closeModalAvance () {
            const TIMEOUT = 100;
            $uibModalInstance.close();
            $timeout(() => {
              $("#vulnerabilities").bootstrapTable("load", auxiliar);
            }, TIMEOUT);
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
