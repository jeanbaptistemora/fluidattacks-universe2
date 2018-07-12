/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, i:true, j:true,
nonexploitLabel:true, totalHigLabel:true, exploitable:true, totalSegLabel:true,
openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg,
userName, userEmail, Rollbar, aux:true, json:true, closeLabel:true, angular,
mixPanelDashboard, win:true, Organization, projectData:true, eventsData:true
*/
/* eslint-env node*/
/**
 * @file ProjectCtrl.js
 * @author engineering@fluidattacks.com
 */
/* Table Formatter */

/**
 * Controller definition for indicators tab view.
 * @name ProjectCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "projectIndicatorsCtrl",
  function projectIndicatorsCtrl (
    $location,
    $scope,
    $state,
    $stateParams,
    $timeout,
    $translate,
    $uibModal,
    functionsFtry1,
    functionsFtry3,
    functionsFtry4,
    projectFtry,
    projectFtry2
  ) {
    const PERCENTAGE_FACTOR = 100;
    const MAX_DECIMALS = 2;
    $scope.init = function init () {
      const projectName = $stateParams.project;
      const findingId = $stateParams.finding;
      $scope.userRole = userRole;
      functionsFtry4.verifyRoles($scope, projectName, userEmail, userRole);
      $scope.view = {};
      $scope.view.project = false;
      $scope.view.finding = false;
      // Route parameters.
      if (angular.isDefined(findingId)) {
        $scope.findingId = findingId;
      }
      if (angular.isDefined(projectName) &&
                projectName !== "") {
        $scope.project = projectName;
        $scope.search();
        const org = Organization.toUpperCase();
        const projt = projectName.toUpperCase();
        angular.element(".equalWidgetHeight").matchHeight();
        mixPanelDashboard.trackReports(
          "ProjectIndicators",
          userName,
          userEmail,
          org,
          projt
        );
      }
      // Search function assignation to button and enter key configuration.
      functionsFtry3.configKeyboardView($scope);
      $scope.goUp();
      $scope.finding = {};
    };
    $scope.goUp = function goUp () {
      angular.element("html, body").animate({"scrollTop": 0}, "fast");
    };
    $scope.calculateCardinality = function calculateCardinality (data) {
      const cardinalityValues = projectFtry2.calCardinality(data);
      $scope.metricsList = [];
      const cardIndex2 = 2;
      const cardIndex3 = 3;
      const cardIndex4 = 4;
      const cardIndex5 = 5;
      const cardIndex6 = 6;
      for (let val = 0; val < cardinalityValues[cardIndex2].length; val++) {
        const color = cardinalityValues[cardIndex2][val].replace(";", "");
        $scope.metricsList.push({
          "color": `${color}`,
          "description": $translate.instant(`${"search_findings.filter_labels" +
                                    "."}${cardinalityValues[cardIndex3][val]}`),
          "icon": cardinalityValues[cardIndex4][val],
          "tooltip": $translate.instant(`${"search_findings.filter_labels" +
                                    "."}${cardinalityValues[cardIndex5][val]}`),
          "value": `${cardinalityValues[cardIndex6][val]}`
        });
      }
      let severity = 0;
      angular.forEach(data.data, (cont) => {
        try {
          if (cont.finding_type === "Seguridad") {
            const BaseScore = projectFtry.calCCssv2(cont)[0];
            severity += BaseScore * parseFloat(cont.cardinalidad_total);
          }
        }
        catch (err) {
          Rollbar.error("Error: An error ocurred calculating cardinality", err);
        }
      });
      const req = projectFtry.totalSeverity($scope.project.toLowerCase());
      req.then((response) => {
        if (!response.error) {
          if (angular.isUndefined(response.data)) {
            location.reload();
          }
          if (response.data.length > 0) {
            const LINES_DIVISOR = 1000;
            const sevConst1 = 4.611;
            const sevConst2 = 43.221;
            const sevConst3 = 4;
            for (let cont = 0; cont < response.data.length; cont++) {
              const target = (parseInt(response.data[cont].lines, 10) /
                             LINES_DIVISOR) +
                             (parseInt(response.data[cont].fields, 10) /
                             sevConst3);
              const totalSeverity = severity / ((sevConst1 * target) +
                                    sevConst2) * PERCENTAGE_FACTOR;
              $scope.metricsList.push({
                "color": "#ef4c43",
                "description": $translate.instant("search_findings." +
                                                  "filter_labels.criticity"),
                "icon": "s7-graph1",
                "tooltip": $translate.instant("search_findings.filter_labels." +
                                                  "criticityTooltip"),
                "value": "n%".replace("n", totalSeverity.toFixed(0))
              });
              $scope.metricsList.push({
                "color": "#00cb77",
                "description": $translate.instant("search_findings." +
                                            "filter_labels.closure"),
                "icon": "s7-like2",
                "tooltip": $translate.instant("search_findings.filter_labels." +
                                            "closureTooltip"),
                "value": "n%".replace("n", Math.round((1 -
                                (cardinalityValues[0] /
                                cardinalityValues[1])) *
                                PERCENTAGE_FACTOR).toString())
              });
            }
          }
          else {
            const totalSeverity = severity;
            $scope.metricsList.push({
              "color": "#ef4c43",
              "description": $translate.instant("search_findings." +
                                                "filter_labels.criticity"),
              "icon": "s7-graph1",
              "tooltip": $translate.instant("search_findings.filter_labels." +
                                                  "criticityTooltip"),
              "value": totalSeverity.toFixed(0)
            });
            $scope.metricsList.push({
              "color": "#00cb77",
              "description": $translate.instant("search_findings." +
                                                "filter_labels.closure"),
              "icon": "s7-like2",
              "tooltip": $translate.instant("search_findings.filter_labels." +
                                                  "closureTooltip"),
              "value": "n%".replace("n", Math.round((1 -
                                    (cardinalityValues[0] /
                                    cardinalityValues[1])) *
                                    PERCENTAGE_FACTOR).toString())
            });
          }
        }
      });
    };
    $scope.mainGraphtypePieChart = function mainGraphtypePieChart () {
      const currData = $scope.data;
      let totalSeg = 0;
      let totalHig = 0;
      angular.forEach(currData, (val) => {
        const type = val.finding_type;
        if (val.estado !== "Cerrado" && val.estado !== "Closed") {
          if (type === "Seguridad") {
            totalSeg += 1;
          }
          else {
            totalHig += 1;
          }
        }
      });
      const segTransl = $translate.instant("grapType.seg_label");
      const higTransl = $translate.instant("grapType.hig_label");
      const totalSegLabel = segTransl + " :n%".replace(":n", (totalSeg *
                            PERCENTAGE_FACTOR / (totalSeg +
                            totalHig)).toFixed(MAX_DECIMALS).toString());
      const totalHigLabel = higTransl + " :n%".replace(":n", (totalHig *
                            PERCENTAGE_FACTOR / (totalSeg +
                            totalHig)).toFixed(MAX_DECIMALS).toString());
      angular.element("#grapType").empty();
      Morris.Donut({ /* eslint-disable-line new-cap */
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
      angular.forEach(currData, (val) => {
        const exploitable = val.exploitability;
        if (val.estado !== "Cerrado" && val.estado !== "Closed") {
          if (exploitable === "1.000 | Alta: No se requiere exploit o se" +
                            " puede automatizar" || exploitable === "0.950 | " +
                             "Funcional: Existe exploit" || exploitable ===
                             "1.000 | High: Exploit is not required or it can" +
                             " be automated" || exploitable === "0.950 | " +
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
      const exploitLabel = exploitTransl + " :n%".replace(
        ":n",
        (exploit * PERCENTAGE_FACTOR / (exploit +
                           nonexploit)).toFixed(MAX_DECIMALS).toString()
      );
      const nonexploitLabel = nonExploitTransl + " :n%".replace(
        ":n",
        (nonexploit * PERCENTAGE_FACTOR / (exploit +
                              nonexploit)).toFixed(MAX_DECIMALS).toString()
      );
      angular.element("#grapExploit").empty();
      Morris.Donut({ /* eslint-disable-line new-cap */
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
      const metricsData = $scope.metricsList;
      let total = 0;
      let open = 0;
      let close = 0;
      let metricName = "";
      angular.forEach(metricsData, (val) => {
        metricName = "search_findings.filter_labels.vulnerabilities";
        if (val.description === $translate.instant(metricName)) {
          total = val.value;
        }
        metricName = "search_findings.filter_labels.cardinalities";
        if (val.description === $translate.instant(metricName)) {
          open = val.value;
        }
      });
      close = total - open;
      total = parseFloat(total);
      const openTransl = $translate.instant("grapStatus.open_label");
      const closeTransl = $translate.instant("grapStatus.close_label");
      const openLabel = openTransl + " :n%".replace(":n", (open *
                   PERCENTAGE_FACTOR / total).toFixed(MAX_DECIMALS).toString());
      const closeLabel = closeTransl + " :n%".replace(":n", (close *
                   PERCENTAGE_FACTOR / total).toFixed(MAX_DECIMALS).toString());
      angular.element("#grapStatus").empty();
      Morris.Donut({ /* eslint-disable-line new-cap */
        "data": [
          {
            "color": "#ff1a1a",
            "label": openLabel,
            "value": open
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
      const projectName = $scope.project;
      const tableFilter = $scope.filter;
      if (angular.isUndefined(projectName) ||
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

        // Handling presentation button
        const searchAt = $translate.instant("proj_alerts.search_title");
        const searchAc = $translate.instant("proj_alerts.search_cont");
        $msg.info(searchAc, searchAt);
        if (eventsData.length === 0 || (eventsData.length > 0 &&
                   eventsData[0].fluidProject.toLowerCase() !==
                   $scope.project.toLowerCase())) {
          const reqEventualities = projectFtry.eventualityByName(
            projectName,
            "Name"
          );
          reqEventualities.then((response) => {
            if (!response.error) {
              if (angular.isUndefined(response.data)) {
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
            projectData[0].fluidProject.toLowerCase() ===
            $scope.project.toLowerCase()) {
          $scope.view.project = true;
          functionsFtry4.loadIndicatorsContent($scope, projectData);
        }
        else {
          const reqProject = projectFtry.projectByName(
            projectName,
            tableFilter
          );
          reqProject.then((response) => {
            $scope.view.project = true;
            if (!response.error) {
              if (angular.isUndefined(response.data)) {
                location.reload();
              }
              mixPanelDashboard.trackSearch(
                "SearchFinding",
                userEmail,
                projectName
              );
              if (response.data.length === 0 && eventsData.length === 0) {
                if ($scope.isManager) {
                  const reqDrafts = projectFtry2.draftsByName(
                    projectName,
                    tableFilter
                  );
                  reqDrafts.then((resp) => {
                    $scope.view.project = true;
                    if (!resp.error) {
                      if (resp.data.length > 0) {
                        $state.go(
                          "ProjectDrafts",
                          {"project": projectName.toLowerCase()}
                        );
                      }
                    }
                  });
                }
                else {
                  $scope.view.project = false;
                  $scope.view.finding = false;
                  $msg.error($translate.instant("proj_alerts.not_found"));
                }
              }
              else {
                projectData = response.data;
                functionsFtry4.loadIndicatorsContent($scope, projectData);
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
    $scope.urlIndicators = function urlIndicators () {
      $state.go("ProjectIndicators", {"project": $scope.project});
    };
    $scope.urlFindings = function urlFindings () {
      $state.go("ProjectFindings", {"project": $scope.project});
    };
    $scope.urlEvents = function urlEvents () {
      $state.go("ProjectEvents", {"project": $scope.project});
    };
    $scope.urlUsers = function urlUsers () {
      $state.go("ProjectUsers", {"project": $scope.project});
    };
    $scope.urlDrafts = function urlDrafts () {
      $state.go("ProjectDrafts", {"project": $scope.project});
    };
    $scope.init();
  }
);
