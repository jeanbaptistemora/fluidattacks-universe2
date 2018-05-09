/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1]}]*/
/* global integrates, BASE, $xhr, window.location:true, response:true,
Organization, mixPanelDashboard, mixPanelDashboard, mixPanelDashboard,$msg,
$, Rollbar, eventsData, userEmail, userName, fieldsToTranslate, keysToTranslate,
findingData, userRole */
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
integrates.factory(
  "functionsFtry3",
  (
    $q, $translate, projectFtry,
    $uibModal, $stateParams, $timeout,
    functionsFtry1, functionsFtry2
  ) => ({

    "configKeyboardView" ($scope) {
      document.onkeypress = function onkeypress (ev) {
        const enterKey = 13;
        if (ev.keyCode === enterKey) {
          if ($("#project").is(":focus")) {
            $scope.search();
          }
        }
      };
    },

    "findingSolved" ($scope) {
    // Obtener datos
      const descData = {
        "findingId": $scope.finding.id,
        "findingName": $scope.finding.hallazgo,
        "findingUrl": window.location.href,
        "findingVulns": $scope.finding.cardinalidad,
        "project": $scope.finding.proyecto_fluid,
        "userMail": userEmail
      };
      const modalInstance = $uibModal.open({

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
            $scope.remediatedData.findingId = mailData.findingId;
            $scope.remediatedData.findingVulns = mailData.findingVulns;
            $scope.remediatedData.justification =
                                $scope.remediatedData.justification.trim();
            if ($scope.remediatedData.justification.length <
                MIN_JUSTIFICATION_LENGTH) {
              $msg.error($translate.instant("proj_alerts." +
                                          "short_remediated_comment"));
            }
            else {
            // Consumir el servicio
              const req = projectFtry.findingSolved($scope.remediatedData);
              // Capturar la Promisse
              req.then((response) => {
                if (!response.error) {
                // Tracking mixpanel
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
                  const ID_GENERATOR_FACTOR_2 = 10000;
                  const INTEGER_BASE = 9;
                  data.id = parseInt(Math.round(new Date() /
                            ID_GENERATOR_FACTOR_1).toString() + (Math.random() *
                            ID_GENERATOR_FACTOR_2).toString(INTEGER_BASE), 10);
                  data.content = $scope.remediatedData.justification;
                  data.parent = 0;
                  data.email = $scope.remediatedData.userMail;
                  data.findingName = $scope.remediatedData.findingName;
                  data.project = $scope.remediatedData.project;
                  data.findingUrl = $scope.remediatedData.findingUrl;
                  data.remediated = true;
                  const comment =
                         projectFtry.addComment(
                           $scope.remediatedData.findingId,
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
        "resolve": {"mailData": descData},
        "templateUrl": `${BASE.url}assets/views/project/remediatedMdl.html`
      });
    },

    "loadFindingContent" ($scope) {
      $scope.aux = {};
      $scope.aux.tratamiento = $scope.finding.tratamiento;
      $scope.aux.razon = $scope.finding.razonTratamiento;
      $scope.aux.cardinalidad = $scope.finding.cardinalidad;
      $scope.hasCompromisedAttributes = true;
      const defineStates = function defineStates () {
        if (typeof $scope.finding.registros === "undefined") {
          $scope.hasCompromisedAttributes = false;
        }
        if ($scope.finding.tratamiento === "Asumido") {
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
        if ($scope.finding.suscripcion === "Continua" ||
            $scope.finding.suscripcion === "Concurrente" ||
            $scope.finding.suscripcion === "Si") {
          $scope.isContinuous = true;
        }
        else {
          $scope.isContinuous = false;
        }
        if ($scope.finding.suscripcion !== "Concurrente" &&
            $scope.finding.suscripcion !== "Puntual" &&
            $scope.finding.suscripcion !== "Continua") {
          Rollbar.warning(`Warning: Finding ${$scope.finding.id} without type`);
        }
      };
      defineStates();
      $scope.aux.responsable = $scope.finding.responsableTratamiento;
      $scope.aux.bts = $scope.finding.btsExterno;
      $scope.severityInfo = {
        "autenticacion": $scope.finding.autenticacion,
        "complejidadAcceso": $scope.finding.complejidadAcceso,
        "explotabilidad": $scope.finding.explotabilidad,
        "id": $scope.finding.id,
        "impactoConfidencialidad": $scope.finding.impactoConfidencialidad,
        "impactoDisponibilidad": $scope.finding.impactoDisponibilidad,
        "impactoIntegridad": $scope.finding.impactoIntegridad,
        "nivelConfianza": $scope.finding.nivelConfianza,
        "nivelResolucion": $scope.finding.nivelResolucion,
        "vectorAcceso": $scope.finding.vectorAcceso
      };
      $scope.descripcionInfo = {
        "actor": $scope.finding.actor,
        "escenario": $scope.finding.escenario
      };
      $scope.finding.hasUrl = $scope.hasUrl($scope.finding.btsExterno);
      $scope.finding.cweIsUrl = $scope.hasUrl($scope.finding.cwe);
      for (let inc = 0; inc < fieldsToTranslate.length; inc++) {
        if ($scope.finding[fieldsToTranslate[inc]] in keysToTranslate) {
          $scope.finding[fieldsToTranslate[inc]] =
                $translate.instant(keysToTranslate[
                  $scope.finding[fieldsToTranslate[inc]]
                ]);
        }
      }
      const NEW_LIST_LIMIT = -3;
      const PERCENTAGE_FACTOR = 100;
      $scope.findingFormatted =
                              $scope.finding.timestamp.slice(0, NEW_LIST_LIMIT);
      let closingEffect = 0;
      for (let close = 0; close < $scope.finding.cierres.length; close++) {
        closingEffect = ($scope.finding.cierres[close].cerradas /
                        $scope.finding.cierres[close].solicitadas) *
                        PERCENTAGE_FACTOR;
        $scope.finding.cierres[close].efectividad = closingEffect.toFixed(0);
        const timeFormat =
               $scope.finding.cierres[close].timestamp.slice(0, NEW_LIST_LIMIT);
        $scope.finding.cierres[close].timestamp = timeFormat;
      }
      // Control de campos para tipos de hallazgo
      $scope.esDetallado = false;
      findingData.esDetallado = $scope.esDetallado;
      if ($scope.finding.nivel === "Detallado") {
        $scope.esDetallado = true;
        findingData.esDetallado = $scope.esDetallado;
      }
      // Control de campos editables
      $scope.onlyReadableTab1 = true;
      $scope.onlyReadableTab2 = true;
      $scope.isManager = userRole !== "customer";
      if (!$scope.isManager && !$scope.isAssumed &&
          !$scope.isClosed && $scope.isContinuous) {
        $(".finding-treatment").show();
      }
      else {
        $(".finding-treatment").hide();
      }
      if ($scope.isManager && $scope.isRemediated) {
        $(".finding-verified").show();
      }
      else {
        $(".finding-verified").hide();
      }
      // Inicializar galeria de evidencias
      $(".popup-gallery").magnificPopup({
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
      if ($("#infoItem").hasClass("active")) {
        $timeout(() => {
          $scope.$broadcast("elastic:adjust");
        });
      }
      $("#trackingItem").on("click", () => {
        $timeout(() => {
          $scope.$broadcast("elastic:adjust");
        });
      });
      $("#infoItem").on("click", () => {
        $timeout(() => {
          $scope.$broadcast("elastic:adjust");
        });
      });
      $("#edit").on("click", () => {
        $timeout(() => {
          $scope.$broadcast("elastic:adjust");
        });
      });
      // Init auto height in panels
      $("#evidenceItem").on("click", () => {
        $(".equalHeight").matchHeight();
      });
      functionsFtry2.findingInformationTab($scope);
      const TIMEOUT = 200;
      $timeout($scope.goUp, TIMEOUT);
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
    },

    "updateDescription" ($scope) {
      // Obtener datos
      const descData = {
        "actor": $scope.descripcionInfo.actor,
        "amenaza": $scope.finding.amenaza,
        "cardinalidad": $scope.finding.cardinalidad,
        "categoria": $scope.finding.categoria,
        "cwe": $scope.finding.cwe,
        "donde": $scope.finding.donde,
        "escenario": $scope.descripcionInfo.escenario,
        "hallazgo": $scope.finding.hallazgo,
        "id": $scope.finding.id,
        "nivel": $scope.finding.nivel,
        "probabilidad": $scope.finding.probabilidad,
        "registros": $scope.finding.registros,
        "registros_num": $scope.finding.registros_num,
        "requisitos": $scope.finding.requisitos,
        "severidad": $scope.finding.severidad,
        "sistema_comprometido": $scope.finding.sistema_comprometido,
        "solucion_efecto": $scope.finding.solucion_efecto,
        "valorRiesgo": $scope.finding.valorRiesgo,
        "vector_ataque": $scope.finding.vector_ataque,
        "vulnerabilidad": $scope.finding.vulnerabilidad
      };
      if ($scope.aux.cardinalidad !== $scope.finding.cardinalidad) {
        const todayDate = new Date();
        const NEW_LIST_LIMIT = 10;
        descData.ultimaVulnerabilidad =
                               todayDate.toISOString().slice(0, NEW_LIST_LIMIT);
      }
      if (descData.nivel === "Detallado") {
        // Recalcular Severidad
        const severityInfo = functionsFtry1.findingCalculateSeveridad();
        const choose = severityInfo[0];
        if (!choose) {
          Rollbar.error("Error: An error occurred calculating severity");
          $msg.error($translate.instant("proj_alerts.wrong_severity"));
          return false;
        }
      }
      const modalInstance = $uibModal.open({
        "animation": true,
        "backdrop": "static",
        "controller" ($scope, $uibModalInstance, updateData) {
          $scope.modalTitle = $translate.instant("confirmmodal." +
                                                 "title_description");
          $scope.ok = function ok () {
            // Consumir el servicio
            const req = projectFtry.updateDescription(updateData);
            // Capturar la Promisse
            req.then((response) => {
              if (!response.error) {
                const updatedAt =
                                 $translate.instant("proj_alerts.updatedTitle");
                const updatedAc =
                                 $translate.instant("proj_alerts.updated_cont");
                $msg.success(updatedAc, updatedAt);
                $uibModalInstance.close();
                location.reload();
                // Tracking mixpanel
                mixPanelDashboard.trackFinding(
                  "UpdateFinding",
                  userEmail,
                  descData.id
                );
              }
              else if (response.error) {
                Rollbar.error("Error: An error occurred updating description");
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
        "resolve": {"updateData": descData},
        "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
      });
      return true;
    }
  })
);
