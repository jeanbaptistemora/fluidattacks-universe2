/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1,3]}]*/
/* global integrates, BASE, $xhr, $window, response:true, Organization, angular,
mixPanelDashboard,$msg, $, Rollbar, eventsData, userEmail, userName, $document,
fieldsToTranslate, keysToTranslate, findingData, userRole, secureRandom */
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "response"] }]*/
/**
 * @file functionsFtry3.js
 * @author engineering@fluidattacks.com
 */
/**
 * Crea el factory de la funcionalidad de hallazgos
 * @name functionsFtry3
 * @param {Object} $q Angular constructor
 * @param {Object} $translate Angular translator
 * @param {Object} projectFtry Factory with main functions
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "functionsFtry3",
  function functionsFtry3Function (
    $document,
    $timeout,
    $translate,
    $uibModal,
    $window,
    functionsFtry1,
    functionsFtry2,
    functionsFtry4,
    projectFtry
  ) {
    return {
      "configKeyboardView" ($scope) {
        $document[0].onkeypress = function onkeypress (ev) {
          const enterKey = 13;
          if (ev.keyCode === enterKey) {
            if (angular.element("#project").is(":focus")) {
              $scope.search();
            }
          }
        };
      },

      "findingHeaderBuilding" ($scope, findingData) {
        $scope.header = {};
        const cierresHallazgo = $scope.finding.cierres;
        const cierresTmp = [];
        for (let cont = 0; cont < cierresHallazgo.length; cont++) {
          const cierre = cierresHallazgo[cont];
          cierre.position = cont + 1;
          cierresTmp.push(cierre);
        }
        $scope.finding.cierres = cierresTmp;
        $scope.header.findingTitle = $scope.finding.finding;
        $scope.header.findingType = $scope.finding.testType;
        $scope.header.findingRisk = "";
        $scope.header.findingState = $scope.finding.estado;
        $scope.header.findingID = $scope.finding.id;
        $scope.header.findingValue = $scope.finding.criticity;
        $scope.header.findingTreatment = $scope.finding.treatment;
        const HIGH_CRITICITY = 7;
        const MODERATE_CRITICITY = 4;
        const findingValue = parseFloat($scope.finding.criticity);
        if (findingValue >= HIGH_CRITICITY) {
          $scope.header.findingValueDescription =
               $translate.instant("finding_formstack.criticity_header.high");
          $scope.header.findingValueColor = $scope.colors.critical;
        }
        else if (findingValue >= MODERATE_CRITICITY &&
               findingValue < HIGH_CRITICITY) {
          $scope.header.findingValueDescription =
            $translate.instant("finding_formstack.criticity_header.moderate");
          $scope.header.findingValueColor = $scope.colors.moderate;
        }
        else {
          $scope.header.findingValueDescription =
            $translate.instant("finding_formstack.criticity_header.tolerable");
          $scope.header.findingValueColor = $scope.colors.tolerable;
        }

        if ($scope.header.findingState === "Abierto" ||
          $scope.header.findingState === "Open") {
          $scope.header.findingStateColor = $scope.colors.critical;
        }
        else if ($scope.header.findingState === "Parcialmente cerrado" ||
               $scope.header.findingState === "Partially closed") {
          $scope.header.findingStateColor = $scope.colors.moderate;
        }
        else {
          $scope.header.findingStateColor = $scope.colors.ok;
        }
        $scope.header.releaseDate = "";
        if ("releaseDate" in $scope.finding) {
          $scope.header.releaseDate = $scope.finding.releaseDate.split(" ")[0];
        }
        $scope.header.findingCount = $scope.finding.openVulnerabilities;
        findingData.header = $scope.header;
      },

      "findingSolved" ($scope) {
      // Obtener datos
        const descData = {
          "findingId": $scope.finding.id,
          "findingName": $scope.finding.finding,
          "findingUrl": $window.location.href,
          "findingVulns": $scope.finding.openVulnerabilities,
          "project": $scope.finding.fluidProject,
          "userMail": userEmail
        };
        $uibModal.open({

          "animation": true,
          "backdrop": "static",
          "controller" ($scope, $uibModalInstance, mailData) {
            $scope.remediatedData = {};
            $scope.modalTitle = $translate.instant("search_findings." +
                                          "tab_description.remediated_finding");
            $scope.ok = function ok () {
              const MIN_JUSTIFICATION_LENGTH = 100;
              $scope.remediatedData.userMail = mailData.userMail;
              $scope.remediatedData.findingName = mailData.findingName;
              $scope.remediatedData.project = mailData.project;
              $scope.remediatedData.findingUrl = mailData.findingUrl;
              $scope.remediatedData.findingVulns = mailData.findingVulns;
              $scope.remediatedData.justification =
                                $scope.remediatedData.justification.trim();
              if ($scope.remediatedData.justification.length <
                MIN_JUSTIFICATION_LENGTH) {
                $msg.error($translate.instant("proj_alerts." +
                                          "short_remediated_comment"));
              }
              else {
                // Make the request
                const req = projectFtry.findingSolved(
                  mailData.findingId,
                  $scope.remediatedData
                );
                // Capture the promise
                req.then((response) => {
                  if (!response.error) {
                  // Mixpanel tracking
                    const org = Organization.toUpperCase();
                    const projt = descData.project.toUpperCase();
                    mixPanelDashboard.trackFindingDetailed(
                      "FindingRemediated",
                      userName,
                      userEmail,
                      org,
                      projt,
                      descData.findingId
                    );
                    $scope.remediated = response.data.remediated;
                    $msg.success(
                      $translate.instant("proj_alerts." +
                                           "remediated_success"),
                      $translate.instant("proj_alerts." +
                                            "updatedTitle")
                    );
                    $uibModalInstance.close();
                    location.reload();
                    const data = {};
                    const ID_GENERATOR_FACTOR_1 = 1000;
                    const ID_GENERATOR_FACTOR_2 = 100;
                    const INTEGER_BASE = 9;
                    data.id = parseInt(Math.round(new Date() /
                            ID_GENERATOR_FACTOR_1).toString() +
                            (parseInt(secureRandom(3).join(""), 10) *
                            ID_GENERATOR_FACTOR_2).toString(INTEGER_BASE), 10);
                    data.content = $scope.remediatedData.justification;
                    data.parent = 0;
                    data.email = $scope.remediatedData.userMail;
                    data.findingName = $scope.remediatedData.findingName;
                    data.project = $scope.remediatedData.project;
                    data.findingUrl = $scope.remediatedData.findingUrl;
                    data.remediated = true;
                    data.commentType = "comment";
                    projectFtry.addComment(
                      mailData.findingId,
                      data
                    );
                  }
                  else if (response.error) {
                    Rollbar.error("Error: An error occurred when " +
                              "remediating the finding");
                    $msg.error($translate.instant("proj_alerts.error_textsad"));
                  }
                });
              }
            };
            $scope.close = function close () {
              $uibModalInstance.close();
            };
          },
          "keyboard": false,
          "resolve": {"mailData": descData},
          "templateUrl": `${BASE.url}assets/views/project/remediatedMdl.html`
        });
      },

      "loadFindingContent" ($scope) {
        $scope.aux = {};
        $scope.aux.treatment = $scope.finding.treatment;
        $scope.aux.razon = $scope.finding.treatmentJustification;
        $scope.aux.openVulnerabilities = $scope.finding.openVulnerabilities;
        $scope.hasCompromisedAttributes = true;
        const defineStates = function defineStates () {
          if (angular.isUndefined($scope.finding.records)) {
            $scope.hasCompromisedAttributes = false;
          }
          if ($scope.finding.treatment === "Asumido") {
            $scope.isAssumed = true;
          }
          else {
            $scope.isAssumed = false;
          }
          if ($scope.finding.estado === "Cerrado") {
            $scope.isClosed = true;
          }
          else {
            $scope.isClosed = false;
          }
          if ($scope.finding.subscription === "Continua" ||
            $scope.finding.subscription === "Concurrente" ||
            $scope.finding.subscription === "Si") {
            $scope.isContinuous = true;
          }
          else {
            $scope.isContinuous = false;
          }
          if ($scope.finding.subscription !== "Concurrente" &&
            $scope.finding.subscription !== "Puntual" &&
            $scope.finding.subscription !== "Continua") {
            Rollbar.warning(`Warning: Finding ${$scope.finding.id} ` +
                            "without type");
          }
        };
        defineStates();
        $scope.aux.responsable = $scope.finding.treatmentManager;
        $scope.aux.bts = $scope.finding.btsExterno;
        $scope.descripcionInfo = {
          "actor": $scope.finding.actor,
          "scenario": $scope.finding.scenario
        };
        $scope.finding.hasUrl = $scope.hasUrl($scope.finding.btsExterno);
        $scope.finding.cweIsUrl = $scope.hasUrl($scope.finding.cwe);

        const NEW_LIST_LIMIT = -3;
        const PERCENTAGE_FACTOR = 100;
        const MIN_DATA_LENGTH = 10;
        if ("releaseDate" in $scope.finding) {
          if ($scope.finding.releaseDate.length > MIN_DATA_LENGTH) {
            $scope.findingFormatted = $scope.finding.
              releaseDate.slice(0, NEW_LIST_LIMIT);
          }
          else {
            $scope.findingFormatted = $scope.finding.releaseDate;
          }
        }
        else {
          $scope.findingFormatted =
                              $scope.finding.timestamp.slice(0, NEW_LIST_LIMIT);
        }
        let closingEffect = 0;
        for (let close = 0; close < $scope.finding.cierres.length; close++) {
          closingEffect = ($scope.finding.cierres[close].closed /
                        $scope.finding.cierres[close].requested) *
                        PERCENTAGE_FACTOR;
          $scope.finding.cierres[close].efectividad = closingEffect.toFixed(0);
          $scope.finding.cierres[close].timeFormat =
               $scope.finding.cierres[close].timestamp.slice(0, NEW_LIST_LIMIT);
        }
        // Fields activation control by finding type (General/Detailed)
        $scope.esDetallado = false;
        findingData.esDetallado = $scope.esDetallado;
        if ($scope.finding.level === "Detallado") {
          $scope.esDetallado = true;
          findingData.esDetallado = $scope.esDetallado;
        }
        // Editable fields control
        $scope.onlyReadableTab1 = true;
        $scope.onlyReadableTab2 = true;
        $scope.isManager = userRole !== "customer" &&
                           userRole !== "customeradmin";
        if ((!$scope.isManager || $scope.isAdmin) && !$scope.isAssumed &&
          !$scope.isClosed && $scope.isContinuous) {
          angular.element(".finding-treatment").show();
        }
        else {
          angular.element(".finding-treatment").hide();
        }
        if ($scope.isManager && $scope.isRemediated) {
          angular.element(".finding-verified").show();
        }
        else {
          angular.element(".finding-verified").hide();
        }
        // Initialize evidence gallery
        angular.element(".popup-gallery").magnificPopup({
          "delegate": "a",
          "gallery": {
            "enabled": true,
            "navigateByImgClick": true,
            "preload": [
              0,
              1
            ]
          },
          "image": {
            "tError": "<a href=\"%url%\">The image #%curr%</a> " +
                    "could not be loaded.",
            "titleSrc" (item) {
              return item.el.attr("title");
            }
          },
          "mainClass": "mfp-img-mobile",
          "tLoading": "Loading image #%curr%...",
          "type": "image"
        });
        // Init auto height in textarea
        if (angular.element("#infoItem").hasClass("active")) {
          $timeout(() => {
            $scope.$broadcast("elastic:adjust");
          });
        }
        angular.element("#trackingItem").on("click", () => {
          $timeout(() => {
            $scope.$broadcast("elastic:adjust");
          });
        });
        angular.element("#infoItem").on("click", () => {
          $timeout(() => {
            $scope.$broadcast("elastic:adjust");
          });
        });
        angular.element("#edit").on("click", () => {
          $timeout(() => {
            $scope.$broadcast("elastic:adjust");
          });
        });
        // Init auto height in panels
        angular.element("#evidenceItem").on("click", () => {
          angular.element(".equalHeight").matchHeight();
        });
        functionsFtry2.findingInformationTab($scope);
        const TIMEOUT = 200;
        $timeout($scope.goUp, TIMEOUT);
        if (!$scope.isManager) {
          $scope.openEvents = projectFtry.alertEvents(eventsData);
          $scope.atAlert = $translate.instant("main_content.eventualities." +
                                            "descSingularAlert1");
          if ($scope.openEvents === 1) {
            $scope.descAlert1 = $translate.instant("main_content." +
                                            "eventualities.descSingularAlert2");
            $scope.descAlert2 = $translate.instant("main_content." +
                                            "eventualities.descSingularAlert3");
            angular.element("#events_alert").show();
          }
          else if ($scope.openEvents > 1) {
            $scope.descAlert1 = $translate.instant("main_content." +
                                              "eventualities.descPluralAlert1");
            $scope.descAlert2 = $translate.instant("main_content." +
                                              "eventualities.descPluralAlert2");
            angular.element("#events_alert").show();
          }
        }
        functionsFtry4.showVulnerabilities($scope);
      },

      "updateDescription" ($scope) {
      // Get actual data
        const descData = {
          "actor": $scope.descripcionInfo.actor,
          "affectedSystems": $scope.finding.affectedSystems,
          "attackVector": $scope.finding.attackVector,
          "category": $scope.finding.category,
          "cwe": $scope.finding.cwe,
          "effectSolution": $scope.finding.effectSolution,
          "finding": $scope.finding.finding,
          "id": $scope.finding.id,
          "level": $scope.finding.level,
          "openVulnerabilities": $scope.finding.openVulnerabilities,
          "probability": $scope.finding.probability,
          "records": $scope.finding.records,
          "recordsNumber": $scope.finding.recordsNumber,
          "requirements": $scope.finding.requirements,
          "riskValue": $scope.finding.riskValue,
          "scenario": $scope.descripcionInfo.scenario,
          "severity": $scope.finding.severity,
          "threat": $scope.finding.threat,
          "vulnerability": $scope.finding.vulnerability,
          "where": $scope.finding.where
        };
        if ($scope.aux.openVulnerabilities !==
            $scope.finding.openVulnerabilities) {
          const todayDate = new Date();
          const NEW_LIST_LIMIT = 10;
          descData.lastVulnerability =
                               todayDate.toISOString().slice(0, NEW_LIST_LIMIT);
        }
        if (descData.level === "Detallado") {
        // Recalculate severity
          const severityInfo = functionsFtry1.calculateFindingSeverity();
          const choose = severityInfo[0];
          if (!choose) {
            Rollbar.error("Error: An error occurred calculating severity");
            $msg.error($translate.instant("proj_alerts.wrong_severity"));
            return false;
          }
        }
        $uibModal.open({
          "animation": true,
          "backdrop": "static",
          "controller" ($scope, $uibModalInstance, updateData) {
            $scope.modalTitle = $translate.instant("confirmmodal." +
                                                 "title_description");
            $scope.ok = function ok () {
              // Make the request
              const req =
                       projectFtry.updateDescription(updateData, updateData.id);
              // Capture the promise
              req.then((response) => {
                if (!response.error) {
                  const updatedAt =
                                 $translate.instant("proj_alerts.updatedTitle");
                  const updatedAc =
                                 $translate.instant("proj_alerts.updated_cont");
                  $msg.success(updatedAc, updatedAt);
                  $uibModalInstance.close();
                  location.reload();
                  // Mixpanel tracking
                  mixPanelDashboard.trackFinding(
                    "UpdateFinding",
                    userEmail,
                    descData.id
                  );
                }
                else if (response.error) {
                  Rollbar.error("Error: An error occurred " +
                                "updating description");
                  const errorAc1 =
                               $translate.instant("proj_alerts.error_textsad");
                  $msg.error(errorAc1);
                }
              });
            };
            $scope.close = function close () {
              $uibModalInstance.close();
            };
          },
          "keyboard": false,
          "resolve": {"updateData": descData},
          "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
        });
        return true;
      }
    };
  }
);
