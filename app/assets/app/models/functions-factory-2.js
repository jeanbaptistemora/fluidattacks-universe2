/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1,2,3,5,6,9,100.0,
                                                   500,1000,10000] }]*/
/* global integrates, BASE, $xhr, window.location:true, response:true,
Organization, mixPanelDashboard, mixPanelDashboard, mixPanelDashboard,$msg,
$, Rollbar, eventsData, userEmail, userName */
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "response"] }]*/
/**
 * @file functions-factory-2.js
 * @author engineering@fluidattacks.com
 */
/**
 * Crea el factory de la funcionalidad de hallazgos
 * @name functionsFtry2
 * @param {Object} $q Angular constructor
 * @param {Object} $translate Angular translator
 * @param {Object} projectFtry Factory with main functions
 * @return {undefined}
 */
/** @export */
integrates.factory(
  "functionsFtry2",
  ($q, $translate, projectFtry, $uibModal, $stateParams) => ({

    "updateCSSv2" ($scope) {
      // Obtener datos de las listas
      const cssv2Data = {

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
      // Recalcular CSSV2
      $scope.findingCalculateCSSv2();
      cssv2Data.criticidad = $scope.finding.criticidad;
      // Instanciar modal de confirmacion
      const modalInstance = $uibModal.open({
        "animation": true,
        "backdrop": "static",
        "controller" ($scope, $uibModalInstance, updateData) {
          $scope.modalTitle = $translate.instant("confirmmodal.title_cssv2");
          $scope.ok = function ok () {
            // Consumir el servicio
            const req = projectFtry.updateCSSv2(updateData);
            // Capturar la Promisse
            req.then((response) => {
              if (!response.error) {
                const updatedAt = $translate.instant("proj_alerts." +
                                                     "updatedTitle");
                const updatedAc = $translate.instant("proj_alerts." +
                                                     "updated_cont");
                $msg.success(updatedAc, updatedAt);
                $uibModalInstance.close();
                location.reload();
              }
              else if (response.error) {
                const errorAc1 = $translate.instant("proj_alerts." +
                                                   "error_textsad");
                Rollbar.error("Error: An error occurred updating CSSv2");
                $msg.error(errorAc1);
              }
            });
          };
          $scope.close = function close () {
            $uibModalInstance.close();
          };
        },
        "resolve": {"updateData": cssv2Data},
        "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
      });
    },

    "updateEvidencesFiles" (element, $scope) {
      let errorAc1 = " ";
      const evImage = $(element).attr("target");
      const dataP = {};
      dataP.document = $(`#evidence${evImage}`).val();
      if (dataP.document === "") {
        errorAc1 = $translate.instant("proj_alerts.error_textsad");
        $msg.error(errorAc1);
        return false;
      }
      const data = new FormData();
      const fileInput = $(`#evidence${evImage}`)[0];
      data.append("id", evImage);
      data.append("url", `${$stateParams.project.toLowerCase()}-` +
                         `${$scope.finding.id}`);
      data.append("findingId", $scope.finding.id);
      data.append("document", fileInput.files[0]);
      const fileName = fileInput.files[0].name;
      const dots = fileName.split(".");
      const fileType = `.${dots[dots.length - 1]}`;
      const pngMaxSize = 2097152;
      const gifMaxSize = 10485760;
      const pyMaxSize = 1048576;
      const csvMaxSize = 1048576;
      if ((fileType === ".png" || fileType === ".PNG") &&
           fileInput.files[0].size > pngMaxSize) {
        errorAc1 = $translate.instant("proj_alerts.file_size_png");
        $msg.error(errorAc1);
        return false;
      }
      if ((fileType === ".gif" || fileType === ".GIF") &&
           fileInput.files[0].size > gifMaxSize) {
        errorAc1 = $translate.instant("proj_alerts.file_size");
        $msg.error(errorAc1);
        return false;
      }
      if ((fileType === ".py" || fileType === ".PY") &&
           fileInput.files[0].size > pyMaxSize) {
        errorAc1 = $translate.instant("proj_alerts.file_size_py");
        $msg.error(errorAc1);
        return false;
      }
      if ((fileType === ".csv" || fileType === ".CSV") &&
           fileInput.files[0].size > csvMaxSize) {
        errorAc1 = $translate.instant("proj_alerts.file_size_py");
        $msg.error(errorAc1);
        return false;
      }
      const evImages = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6"
      ];
      if (evImage === "0" && (fileType !== ".gif" && fileType !== ".GIF")) {
        errorAc1 = $translate.instant("proj_alerts.file_type_gif");
        $msg.error(errorAc1);
        return false;
      }
      else if (evImage === "7" && (fileType !== ".py" && fileType !== ".PY")) {
        errorAc1 = $translate.instant("proj_alerts.file_type_py");
        $msg.error(errorAc1);
        return false;
      }
      else if (evImage === "8" &&
                    (fileType !== ".csv" && fileType !== ".CSV")) {
        errorAc1 = $translate.instant("proj_alerts.file_type_csv");
        $msg.error(errorAc1);
        return false;
      }
      else if (evImages.indexOf(evImage) !== -1 && (fileType !== ".png" &&
               fileType !== ".PNG")) {
        errorAc1 = $translate.instant("proj_alerts.file_type_png");
        $msg.error(errorAc1);
        return false;
      }
      const responseFunction = function responseFunction (response) {
        if (!response.error) {
          const updatedAt = $translate.instant("proj_alerts.updatedTitle");
          const updatedAc = $translate.instant("proj_alerts.updated_cont_file");
          $msg.success(updatedAc, updatedAt);
          location.reload();
          return true;
        }
        errorAc1 = $translate.instant("proj_alerts.no_file_update");
        Rollbar.error("Error: An error occurred updating evidences");
        $msg.error(errorAc1);
        return false;
      };
      const errorFunction = function errorFunction (response) {
        if (!response.error) {
          errorAc1 = $translate.instant("proj_alerts.no_file_update");
          Rollbar.error("Error: An error occurred updating evidences");
          $msg.error(errorAc1);
          return false;
        }
        return true;
      };
      projectFtry.updateEvidenceFiles(data, responseFunction, errorFunction);
      return true;
    }
  })
);
