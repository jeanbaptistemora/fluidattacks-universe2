/* eslint-disable max-lines */
/* eslint no-magic-numbers:
["error", { "ignore": [-3,-1,0,0.4,0.6,1,1.176,1.5,2,3,
                       4,5,6,6.9,7,9,10,10.41,20,50,
                       80,100,200,500,1000,10000] }]*/
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "$state","response"] }]*/
/* global
BASE, document, $, $msg, userName, integrates, userEmail, userName, Rollbar,
mixPanelDashboard, userRole, findingType, actor, scenario, authentication,
confidenciality, Organization, resolutionLevel, explotability, availability,
tratamiento, updateEvidencesFiles:true, findingData:true, realiabilityLevel,
updateEvidenceText:true, categories, probabilities, accessVector, integrity,
accessComplexity, projectData:true, eventsData:true, fieldsToTranslate,
keysToTranslate, desc:true */
/**
 * @file findingcontentCtrl.js
 * @author engineering@fluidattacks.com
 */
/**
 * Funciones para administrar el UI del resumen de un hallazgo
 * @name findingContentCtrl.js
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $translate
 * @param {Object} ngNotify
 * @return {undefined}
 */
/** @export */
integrates.controller("findingcontentCtrl", function findingcontentCtrl (
  $scope, $stateParams, $timeout,
  $uibModal, $translate, $state,
  ngNotify, projectFtry, findingFtry
) {
  $scope.findingHeaderBuilding = function findingHeaderBuilding () {
    $scope.header = {};
    const cierresHallazgo = $scope.finding.cierres;
    const cierresTmp = [];
    for (let cont = 0; cont < cierresHallazgo.length; cont++) {
      const cierre = cierresHallazgo[cont];
      cierre.position = cont + 1;
      cierresTmp.push(cierre);
    }
    $scope.finding.cierres = cierresTmp;
    $scope.header.findingTitle = $scope.finding.hallazgo;
    $scope.header.findingType = $scope.finding.tipoPrueba;
    $scope.header.findingRisk = "";
    $scope.header.findingState = $scope.finding.estado;
    $scope.header.findingID = $scope.finding.id;
    $scope.header.findingValue = $scope.finding.criticidad;
    $scope.header.findingTreatment = $scope.finding.tratamiento;
    const findingValue = parseFloat($scope.finding.criticidad);
    if (findingValue >= 7) {
      $scope.header.findingValueDescription =
             $translate.instant("finding_formstack.criticity_header.high");
      $scope.header.findingValueColor = $scope.colors.critical;
    }
    else if (findingValue >= 4 && findingValue <= 6.9) {
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

    $scope.header.findingCount = $scope.finding.cardinalidad;
    findingData.header = $scope.header;
  };
  String.prototype.replaceAll = function replaceAll (
    search,
    replace
  ) { /* eslint no-extend-native: ["error", { "exceptions": ["String"] }]*/
    if (typeof replace === "undefined") {
      return this.toString();
    }
    return this.replace(new RegExp(`[${search}]`, "g"), replace);
  };
  $scope.alertHeader = function alertHeader (company, project) {
    const req = projectFtry.getAlerts(company, project);
    req.then((response) => {
      if (!response.error && response.data.length > 0) {
        if (response.data[0].status_act === "1") {
          let html = "<div class=\"alert alert-danger-2\">";
          html += "<strong>Atención! </strong>" +
                  `${response.data[0].message}</div>`;
          document.getElementById("header_alert").innerHTML = html;
        }
      }
    });
  };
  $scope.cssv2Editable = function cssv2Editable () {
    if ($scope.onlyReadableTab2 === false) {
      $scope.onlyReadableTab2 = true;
    }
    else {
      $scope.onlyReadableTab2 = false;
    }
  };
  $scope.descriptionEditable = function descriptionEditable () {
    if ($scope.onlyReadableTab1 === false) {
      $scope.onlyReadableTab1 = true;
    }
    else {
      $scope.onlyReadableTab1 = false;
    }
  };
  $scope.evidenceEditable = function evidenceEditable () {
    if ($scope.onlyReadableTab3 === false) {
      $scope.onlyReadableTab3 = true;
    }
    else {
      $scope.onlyReadableTab3 = false;
    }
    const inputs = document.querySelectorAll(".inputfile");
    Array.prototype.forEach.call(inputs, (input) => {
      const label = input.nextElementSibling;
      const labelVal = label.innerHTML;

      input.addEventListener("change", (aux) => {
        let fileName = "";
        if (input.files && input.files.length > 1) {
          fileName = (input.getAttribute("data-multiple-caption") ||
                      "").replace("{count}", input.files.length);
        }
        else {
          fileName = aux.target.value.split("\\").pop();
        }

        if (fileName) {
          label.querySelector("span").innerHTML = fileName;
        }
        else {
          label.innerHTML = labelVal;
        }
      });

      // Firefox bug fix
      input.addEventListener("focus", () => {
        input.classList.add("has-focus");
      });
      input.addEventListener("blur", () => {
        input.classList.remove("has-focus");
      });
    });
    $scope.evidenceDescription = [
      $("#evidenceText0").val(),
      $("#evidenceText1").val(),
      $("#evidenceText2").val(),
      $("#evidenceText3").val(),
      $("#evidenceText4").val(),
      $("#evidenceText5").val(),
      $("#evidenceText6").val()
    ];
    const refList = [];
    for (let cont = 0; cont < $scope.tabEvidences.length; cont++) {
      refList.push($scope.tabEvidences[cont].ref);
    }
    const evidencesList = [];
    if (refList.indexOf(0) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": $translate.instant("search_findings." +
                                   "tab_evidence.animation_exploit"),
        "ref": 0
      });
    }
    if (refList.indexOf(1) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": $translate.instant("search_findings." +
                                   "tab_evidence.evidence_exploit"),
        "ref": 1
      });
    }
    if (refList.indexOf(2) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": `${$translate.instant("search_findings." +
                                      "tab_evidence.evidence_name")} 1`,
        "ref": 2
      });
    }
    if (refList.indexOf(3) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": `${$translate.instant("search_findings." +
                                      "tab_evidence.evidence_name")} 2`,
        "ref": 3
      });
    }
    if (refList.indexOf(4) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": `${$translate.instant("search_findings." +
                                      "tab_evidence.evidence_name")} 3`,
        "ref": 4
      });
    }
    if (refList.indexOf(5) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": `${$translate.instant("search_findings." +
                                      "tab_evidence.evidence_name")} 4`,
        "ref": 5
      });
    }
    if (refList.indexOf(6) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": `${$translate.instant("search_findings." +
                                      "tab_evidence.evidence_name")} 5`,
        "ref": 6
      });
    }
    $scope.tabEvidences.sort((auxa, auxb) => auxa.ref - auxb.ref);
  };
  $scope.treatmentEditable = function treatmentEditable () {
    $scope.goDown();
    if ($scope.onlyReadableTab4 === false) {
      $scope.finding.responsableTratamiento = userEmail;
      $scope.onlyReadableTab4 = true;
      $scope.finding.tratamiento = $scope.aux.tratamiento;
      $scope.finding.razonTratamiento = $scope.aux.razon;
      $scope.finding.btsExterno = $scope.aux.bts;
    }
    else if ($scope.onlyReadableTab4 === true) {
      $scope.finding.tratamiento = $scope.aux.tratamiento;
      $scope.finding.razonTratamiento = $scope.aux.razon;
      $scope.finding.responsableTratamiento = $scope.aux.responsable;
      $scope.finding.btsExterno = $scope.aux.bts;
      $scope.onlyReadableTab4 = false;
    }
  };
  $scope.exploitEditable = function exploitEditable () {
    if ($scope.onlyReadableTab5 === false) {
      $scope.onlyReadableTab5 = true;
    }
    else {
      $scope.onlyReadableTab5 = false;
    }
    const inputs = document.querySelectorAll(".inputfile");
    Array.prototype.forEach.call(inputs, (input) => {
      const label = input.nextElementSibling;
      const labelVal = label.innerHTML;

      input.addEventListener("change", (err) => {
        let fileName = "";
        if (input.files && input.files.length > 1) {
          fileName = (input.getAttribute("data-multiple-caption") ||
                      "").replace("{count}", input.files.length);
        }
        else {
          fileName = err.target.value.split("\\").pop();
        }

        if (fileName) {
          label.querySelector("span").innerHTML = fileName;
        }
        else {
          label.innerHTML = labelVal;
        }
      });

      // Firefox bug fix
      input.addEventListener("focus", () => {
        input.classList.add("has-focus");
      });
      input.addEventListener("blur", () => {
        input.classList.remove("has-focus");
      });
    });
  };
  $scope.recordsEditable = function recordsEditable () {
    if ($scope.onlyReadableTab6 === false) {
      $scope.onlyReadableTab6 = true;
    }
    else {
      $scope.onlyReadableTab6 = false;
    }
    const inputs = document.querySelectorAll(".inputfile");
    Array.prototype.forEach.call(inputs, (input) => {
      const label = input.nextElementSibling;
      const labelVal = label.innerHTML;

      input.addEventListener("change", (err) => {
        let fileName = "";
        if (input.files && input.files.length > 1) {
          fileName = (input.getAttribute("data-multiple-caption") ||
                      "").replace("{count}", input.files.length);
        }
        else {
          fileName = err.target.value.split("\\").pop();
        }

        if (fileName) {
          label.querySelector("span").innerHTML = fileName;
        }
        else {
          label.innerHTML = labelVal;
        }
      });

      // Firefox bug fix
      input.addEventListener("focus", () => {
        input.classList.add("has-focus");
      });
      input.addEventListener("blur", () => {
        input.classList.remove("has-focus");
      });
    });
  };
  $scope.detectNivel = function detectNivel () {
    $timeout(() => {
      $scope.$apply();
      if ($scope.finding.nivel === "Detallado") {
        $scope.esDetallado = true;
        findingData.esDetallado = $scope.esDetallado;
      }
      else {
        $scope.esDetallado = false;
        findingData.esDetallado = $scope.esDetallado;
      }
    }, 200);
  };
  $scope.updateCSSv2 = function updateCSSv2 () {
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
              const updatedAt = $translate.instant("proj_alerts.updatedTitle");
              const updatedAc = $translate.instant("proj_alerts.updated_cont");
              $msg.success(updatedAc, updatedAt);
              $uibModalInstance.close();
              location.reload();
            }
            else if (response.error) {
              const errorAc1 = $translate.instant("proj_alerts.error_textsad");
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
  };
  updateEvidencesFiles = function updateEvidencesFiles (element) {
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
    else if (evImage === "8" && (fileType !== ".csv" && fileType !== ".CSV")) {
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
  };
  updateEvidenceText = function updateEvidenceText (element) {
    const evImage = $(element).attr("target");
    const data = {};
    data.id = $scope.finding.id;
    const description = $(`#evidenceText${evImage}`).val();
    const file = $(`#evidence${evImage}`).val();
    if (description === "" || $scope.evidenceDescription[evImage] ===
        description) {
      if (file !== "") {
        updateEvidencesFiles(element);
      }
      else if (file === "") {
        return false;
      }
    }
    else {
      if (evImage === "2") {
        data.descEvidencia1 = description;
        data.field = "descEvidencia1";
      }
      if (evImage === "3") {
        data.descEvidencia2 = description;
        data.field = "descEvidencia2";
      }
      if (evImage === "4") {
        data.descEvidencia3 = description;
        data.field = "descEvidencia3";
      }
      if (evImage === "5") {
        data.descEvidencia4 = description;
        data.field = "descEvidencia4";
      }
      if (evImage === "6") {
        data.descEvidencia5 = description;
        data.field = "descEvidencia5";
      }
      const req = projectFtry.updateEvidenceText(data);
      // Capturar la Promisse
      req.then((response) => {
        if (!response.error) {
          const updatedAt = $translate.instant("proj_alerts.updatedTitle");
          const updatedAc = $translate.instant("proj_alerts." +
                                               "updated_cont_description");
          $msg.success(updatedAc, updatedAt);
          if (file !== "") {
            updateEvidencesFiles(element);
          }
          else if (file === "") {
            location.reload();
          }
          return true;
        }
        const errorAc1 = $translate.instant("proj_alerts.no_text_update");
        Rollbar.error("Error: An error occurred updating " +
                      "evidences description");
        $msg.error(errorAc1);
        return false;
      });
    }
    return true;
  };
  $scope.deleteFinding = function deleteFinding () {
    // Obtener datos
    const descData = {"id": $scope.finding.id};
    const modalInstance = $uibModal.open({
      "animation": true,
      "backdrop": "static",
      "controller" (
        $scope,
        $uibModalInstance,
        updateData,
        $stateParams,
        $state
      ) {
        $scope.vuln = {};
        $scope.modalTitle = $translate.instant("confirmmodal.title_finding");
        $scope.ok = function ok () {
          $scope.vuln.id = updateData.id;
          // Consumir el servicio
          const req = projectFtry.deleteFinding($scope.vuln);
          // Capturar la Promisse
          req.then((response) => {
            if (!response.error) {
              const updatedAt = $translate.instant("proj_alerts.updatedTitle");
              const updatedAc = $translate.instant("proj_alerts.updated_cont");
              $msg.success(updatedAc, updatedAt);
              $uibModalInstance.close();
              $state.go("ProjectFindings", {"project": $stateParams.project});
              // Tracking mixpanel
              mixPanelDashboard.trackFinding(
                "deleteFinding",
                userEmail,
                descData.id
              );
            }
            else if (response.error) {
              const errorAc1 = $translate.instant("proj_alerts.error_textsad");
              Rollbar.error("Error: An error occurred deleting finding");
              $msg.error(errorAc1);
            }
          });
        };
        $scope.close = function close () {
          $uibModalInstance.close();
        };
      },
      "resolve": {"updateData": descData},
      "templateUrl": `${BASE.url}assets/views/project/deleteMdl.html`
    });
  };
  $scope.goUp = function goUp () {
    $("html, body").animate({"scrollTop": 0}, "fast");
  };
  $scope.goDown = function goDown () {
    window.scrollTo(0, document.body.scrollHeight);
  };
  $scope.hasUrl = function hasUrl (element) {
    if (typeof element !== "undefined") {
      if (element.indexOf("https://") !== -1 ||
          element.indexOf("http://") !== -1) {
        return true;
      }
    }
    return false;
  };
  $scope.isEmpty = function isEmpty (obj) {
    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        return false;
      }
    }
    return true;
  };
  $scope.loadFindingByID = function loadFindingByID (id) {
    if (eventsData.length === 0 || (eventsData.length > 0 &&
                   eventsData[0].proyecto_fluid.toLowerCase() !==
                   $stateParams.project.toLowerCase())) {
      const reqEventualities = projectFtry.eventualityByName(
        $stateParams.project,
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
    if (!$scope.isEmpty(findingData) &&
        findingData.data.proyecto_fluid.toLowerCase() ===
        $stateParams.project.toLowerCase() &&
        findingData.data.id === $scope.finding.id) {
      $scope.view.project = false;
      $scope.view.finding = true;
      $scope.finding = findingData.data;
      $scope.header = findingData.header;
      $scope.isRemediated = findingData.remediated;
      $scope.tabEvidences = findingData.tabEvidences;
      $scope.hasExploit = findingData.hasExploit;
      $scope.exploitURL = findingData.exploitURL;
      $scope.hasRecords = findingData.hasRecords;
      $scope.esDetallado = findingData.esDetallado;
      $scope.loadFindingContent();
    }
    else {
      const req = projectFtry.findingById(id);
      req.then((response) => {
        if (!response.error && $stateParams.project ===
            response.data.proyecto_fluid.toLowerCase()) {
          findingData.data = response.data;
          $scope.finding = response.data;
          $scope.loadFindingContent();
          $scope.findingHeaderBuilding();
          $scope.remediatedView();
          findingData.remediated = $scope.isRemediated;
          $scope.view.project = false;
          $scope.view.finding = true;
          $scope.findingEvidenceTab();
          const exploitinfo =
                             findingFtry.findingExploitTab($scope, findingData);
          $scope.hasExploit = exploitinfo[0];
          $scope.exploitURL = exploitinfo[1];
          findingData.hasExploit = exploitinfo[2];
          findingData.exploitURL = exploitinfo[3];
          const recordinfo = findingFtry.findingRecordsTab($scope, findingData);
          $scope.hasRecords = recordinfo[0];
          findingData.hasRecords = recordinfo[1];
          findingFtry.findingCommentTab($scope, $stateParams);
          return true;
        }
        else if (response.error) {
          $scope.view.project = false;
          $scope.view.finding = false;
          if (response.message === "Project masked") {
            Rollbar.warning("Warning: Project deleted");
            $msg.error($translate.instant("proj_alerts.project_deleted"));
          }
          else {
            $msg.error($translate.instant("proj_alerts.no_finding"));
            Rollbar.warning("Warning: Finding not found");
          }
        }
        return true;
      });
    }
  };
  $scope.loadFindingContent = function loadFindingContent () {
    $scope.aux = {};
    $scope.aux.tratamiento = $scope.finding.tratamiento;
    $scope.aux.razon = $scope.finding.razonTratamiento;
    $scope.aux.cardinalidad = $scope.finding.cardinalidad;
    $scope.hasCompromisedAttributes = true;
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
    $scope.aux.responsable = $scope.finding.responsableTratamiento;
    $scope.aux.bts = $scope.finding.btsExterno;
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
    $scope.findingFormatted = $scope.finding.timestamp.slice(0, -3);
    let closingEffect = 0;
    for (let close = 0; close < $scope.finding.cierres.length; close++) {
      closingEffect = ($scope.finding.cierres[close].cerradas /
                      $scope.finding.cierres[close].solicitadas) * 100;
      $scope.finding.cierres[close].efectividad = closingEffect.toFixed(0);
      const timeFormat = $scope.finding.cierres[close].timestamp.slice(0, -3);
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
    $scope.findingInformationTab();
    $timeout($scope.goUp, 200);
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
  $scope.configColorPalette = function configColorPalette () {
    $scope.colors = {};
    // Red
    $scope.colors.critical = "background-color: #f12;";
    // Orange
    $scope.colors.moderate = "background-color: #f72;";
    // Yellow
    $scope.colors.tolerable = "background-color: #ffbf00;";
    // Green
    $scope.colors.ok = "background-color: #008000;";
  };
  $scope.findingCalculateCSSv2 = function findingCalculateCSSv2 () {
    const calCSSv2 = projectFtry.calCCssv2($scope.finding);
    const BaseScore = calCSSv2[0];
    const Temporal = calCSSv2[1];
    const CVSSGeneral = Temporal;
    $scope.finding.cssv2base = BaseScore.toFixed(1);
    $scope.finding.criticidad = Temporal.toFixed(1);
  };
  $scope.findingDropDownList = function findingDropDownList () {
    $scope.list = {};
    $scope.list.findingType = findingType;
    $scope.list.categories = categories;
    $scope.list.probability = probabilities;
    $scope.list.actor = actor;
    $scope.list.scenario = scenario;
    $scope.list.accessVector = accessVector;
    $scope.list.accessComplexity = accessComplexity;
    $scope.list.authentication = authentication;
    $scope.list.confidenciality = confidenciality;
    $scope.list.integrity = integrity;
    $scope.list.availability = availability;
    $scope.list.explotability = explotability;
    $scope.list.resolutionLevel = resolutionLevel;
    $scope.list.realiabilityLevel = realiabilityLevel;
  };
  $scope.findingInformationTab = function findingInformationTab () {
    $scope.findingDropDownList();
    $scope.finding.cardinalidad = parseInt($scope.finding.cardinalidad, 10);
    $scope.finding.criticidad = parseFloat($scope.finding.criticidad);
    $scope.findingCalculateCSSv2();
    if ($scope.finding.nivel === "Detallado") {
      $scope.esDetallado = "show-detallado";
      $scope.esGeneral = "hide-detallado";
      $scope.findingCalculateSeveridad();
    }
    else {
      $scope.esDetallado = "hide-detallado";
      $scope.esGeneral = "show-detallado";
    }
  };
  $scope.capitalizeFirstLetter = function capitalizeFirstLetter (string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };
  $scope.updEvidenceList = function
  updEvidenceList (data, keyU, keyD, ref, type) {
    const urlPre = `${window.location.href.split("dashboard#!/")[0] +
                    window.location.href.split("dashboard#!/")[1]}/`;
    const url = urlPre + data;
    if (type === "basic") {
      $scope.descText =
                  $translate.instant(`search_findings.tab_evidence.${keyU}`);
    }
    else {
      $scope.descText = $scope.finding[keyU];
    }
    $scope.evidenceList.push({
      "desc": $scope.descText,
      "name": $translate.instant(`search_findings.tab_evidence.${keyD}`),
      ref,
      url
    });
  };
  $scope.findingEvidenceTab = function findingEvidenceTab () {
    $scope.tabEvidences = [];
    $scope.evidenceList = [];
    const url = "";
    const urlPre = "";
    const req = projectFtry.getEvidences($scope.finding.id);
    req.then((response) => {
      if (!response.error) {
        const valFormstack = $scope.finding;
        if (response.data.length > 0) {
          for (let cont = 0; cont < response.data.length; cont++) {
            const valS3 = response.data[cont];
            if (typeof valS3.animacion !== "undefined" &&
                        valS3.es_animacion === true) {
              $scope.updEvidenceList(
                valS3.animacion, "animation_exploit",
                "animation_exploit", 0, "basic"
              );
            }
            else if (typeof valFormstack.animacion !== "undefined") {
              $scope.updEvidenceList(
                valFormstack.animacion, "animation_exploit",
                "animation_exploit", 0, "basic"
              );
            }
            if (typeof valS3.explotacion !== "undefined" &&
                       valS3.es_explotacion === true) {
              $scope.updEvidenceList(
                valS3.explotacion, "evidence_exploit",
                "evidence_exploit", 1, "basic"
              );
            }
            else if (typeof valFormstack.explotacion !== "undefined") {
              $scope.updEvidenceList(
                valFormstack.explotacion, "evidence_exploit",
                "evidence_exploit", 1, "basic"
              );
            }
            for (let inc = 1; inc < 6; inc++) {
              if (typeof valFormstack[`desc_evidencia_${inc}`] !==
                "undefined" && typeof valS3[`ruta_evidencia_${inc}`] !==
                "undefined" && valS3[`es_ruta_evidencia_${inc}`] === true) {
                $scope.updEvidenceList(
                  valS3[`ruta_evidencia_${inc}`], `desc_evidencia_${inc}`,
                  "evidence_name", inc + 1, "special"
                );
              }
              else if (typeof valFormstack[`desc_evidencia_${inc}`] !==
                "undefined" && typeof valFormstack[`ruta_evidencia_${inc}`] !==
                "undefined") {
                $scope.updEvidenceList(
                  valFormstack[`ruta_evidencia_${inc}`],
                  `desc_evidencia_${inc}`,
                  "evidence_name", inc + 1, "special"
                );
              }
            }
            $scope.tabEvidences = $scope.evidenceList;
            findingData.tabEvidences = $scope.evidenceList;
          }
        }
        else {
          if (typeof $scope.finding.animacion !== "undefined") {
            $scope.updEvidenceList(
              valFormstack.animacion, "animation_exploit",
              "animation_exploit", 0, "basic"
            );
          }
          if (typeof $scope.finding.explotacion !== "undefined") {
            $scope.updEvidenceList(
              valFormstack.explotacion, "evidence_exploit",
              "evidence_exploit", 1, "basic"
            );
          }
          for (let inc = 1; inc < 6; inc++) {
            if (typeof valFormstack[`desc_evidencia_${inc}`] !== "undefined" &&
                typeof valFormstack[`ruta_evidencia_${inc}`] !== "undefined") {
              $scope.updEvidenceList(
                valFormstack[`ruta_evidencia_${inc}`], `desc_evidencia_${inc}`,
                "evidence_name", inc + 1, "special"
              );
            }
          }
          $scope.tabEvidences = $scope.evidenceList;
          findingData.tabEvidences = $scope.evidenceList;
        }
      }
      else if (response.error) {
        Rollbar.error("Error: An error occurred loading evidences");
        findingData.tabEvidences = $scope.evidenceList;
      }
    });
  };
  $scope.findingCalculateSeveridad = function findingCalculateSeveridad () {
    let severidad = 0;
    if (!isNaN($scope.finding.severidad)) {
      severidad = parseFloat($scope.finding.severidad);
      if (severidad < 0 || severidad > 5) {
        Rollbar.error("Error: Severity must be an integer bewteen 0 and 5");
        $msg.error($translate.instant("proj_alerts.error_severity"), "error");
        return false;
      }
      try {
        let prob = $scope.finding.probabilidad;
        severidad = $scope.finding.severidad;
        prob = prob.split("%")[0];
        prob = parseFloat(prob) / 100.0;
        severidad = parseFloat(severidad);
        const vRiesgo = prob * severidad;
        if (vRiesgo >= 3) {
          $scope.finding.valorRiesgo = "(:r) Critico".replace(
            ":r",
            vRiesgo.toFixed(1)
          );
        }
        else if (vRiesgo >= 2 && vRiesgo < 3) {
          $scope.finding.valorRiesgo = "(:r) Moderado".replace(
            ":r",
            vRiesgo.toFixed(1)
          );
        }
        else {
          $scope.finding.valorRiesgo = "(:r) Tolerable".replace(
            ":r",
            vRiesgo.toFixed(1)
          );
        }
        return true;
      }
      catch (err) {
        $scope.finding.valorRiesgo = "";
        return false;
      }
    }
    else if (isNaN($scope.finding.severidad)) {
      Rollbar.error("Error: Severity must be an integer bewteen 0 and 5");
      $msg.error($translate.instant("proj_alerts.error_severity"), "error");
      return false;
    }
    return true;
  };
  $scope.updateDescription = function updateDescription () {
    // Obtener datos
    const descData = {
      "actor": $scope.finding.actor,
      "amenaza": $scope.finding.amenaza,
      "cardinalidad": $scope.finding.cardinalidad,
      "categoria": $scope.finding.categoria,
      "cwe": $scope.finding.cwe,
      "donde": $scope.finding.donde,
      "escenario": $scope.finding.escenario,
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
      descData.ultimaVulnerabilidad = todayDate.toISOString().slice(0, 10);
    }
    if (descData.nivel === "Detallado") {
      // Recalcular Severidad
      const choose = $scope.findingCalculateSeveridad();
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
              const updatedAt = $translate.instant("proj_alerts.updatedTitle");
              const updatedAc = $translate.instant("proj_alerts.updated_cont");
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
              const errorAc1 = $translate.instant("proj_alerts.error_textsad");
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
  };
  $scope.validateTreatment = function validateTreatment () {
    const minCharacter = 30;
    if ($scope.aux.razon === $scope.finding.razonTratamiento) {
      $msg.error($translate.instant("proj_alerts.differ_comment"));
      return false;
    }
    else if ($scope.finding.razonTratamiento === "") {
      $msg.error($translate.instant("proj_alerts.empty_comment"));
      return false;
    }
    else if ($scope.finding.razonTratamiento.length < minCharacter) {
      $msg.error($translate.instant("proj_alerts.short_comment"));
      return false;
    }
    $scope.finding.responsableTratamiento = userEmail;
    return true;
  };
  $scope.updateTreatment = function updateTreatment () {
    let flag = false;
    if ($scope.aux.tratamiento === $scope.finding.tratamiento &&
        $scope.aux.razon === $scope.finding.razonTratamiento &&
        $scope.aux.bts !== $scope.finding.btsExterno) {
      flag = true;
    }
    else if ($scope.validateTreatment()) {
      flag = true;
    }
    if (flag === true) {
      const newData = {
        "bts_externo": $scope.finding.btsExterno,
        "id": $scope.finding.id,
        "razonTratamiento": $scope.finding.razonTratamiento,
        "responsableTratamiento": $scope.finding.responsableTratamiento,
        "tratamiento": $scope.finding.tratamiento
      };
      const modalInstance = $uibModal.open({
        "animation": true,
        "backdrop": "static",
        "controller" ($scope, $uibModalInstance, updateData) {
          $scope.modalTitle = $translate.instant("search_findings." +
                                                 "tab_description." +
                                                 "update_treatmodal");
          $scope.ok = function ok () {
            // Consumir el servicio
            const req = projectFtry.updateTreatment(updateData);
            // Capturar la Promisse
            req.then((response) => {
              if (!response.error) {
                const org = Organization.toUpperCase();
                const projt = $stateParams.project.toUpperCase();
                mixPanelDashboard.trackFindingDetailed(
                  "FindingUpdateTreatment",
                  userName,
                  userEmail,
                  org,
                  projt,
                  newData.id
                );
                $msg.success(
                  $translate.instant("proj_alerts." +
                                           "updated_treat"),
                  $translate.instant("proj_alerts." +
                                                         "congratulation")
                );
                $uibModalInstance.close();
                location.reload();
              }
              else if (response.error) {
                Rollbar.error("Error: An error occurred updating treatment");
                const errorAc1 = $translate.instant("proj_alerts." +
                                                    "error_textsad");
                $msg.error(errorAc1);
              }
            });
          };
          $scope.close = function close () {
            $uibModalInstance.close();
          };
        },
        "resolve": {"updateData": newData},
        "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
      });
    }
  };
  $scope.findingSolved = function findingSolved () {
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
          $scope.remediatedData.userMail = mailData.userMail;
          $scope.remediatedData.findingName = mailData.findingName;
          $scope.remediatedData.project = mailData.project;
          $scope.remediatedData.findingUrl = mailData.findingUrl;
          $scope.remediatedData.findingId = mailData.findingId;
          $scope.remediatedData.findingVulns = mailData.findingVulns;
          $scope.remediatedData.justification =
                                $scope.remediatedData.justification.trim();
          if ($scope.remediatedData.justification.length < 100) {
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
                data.id = parseInt(Math.round(new Date() / 1000).toString() +
                          (Math.random() * 10000).toString(9), 10);
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
  };
  $scope.remediatedView = function remediatedView () {
    $scope.isManager = userRole !== "customer";
    $scope.isRemediated = true;
    if (typeof $scope.finding.id !== "undefined") {
      const req = projectFtry.remediatedView($scope.finding.id);
      req.then((response) => {
        if (!response.error) {
          $scope.isRemediated = response.data.remediated;
          findingData.remediated = $scope.isRemediated;
          if ($scope.isManager && $scope.isRemediated) {
            $(".finding-verified").show();
          }
          else {
            $(".finding-verified").hide();
          }
        }
        else if (response.error) {
          Rollbar.error("Error: An error occurred when " +
                        "remediating/verifying the finding");
        }
      });
    }
  };
  $scope.findingVerified = function findingVerified () {
    // Obtener datos
    const currUrl = window.location.href;
    const trackingUrl = currUrl.replace("/description", "/tracking");
    const descData = {
      "findingId": $scope.finding.id,
      "findingName": $scope.finding.hallazgo,
      "findingUrl": trackingUrl,
      "findingVulns": $scope.finding.cardinalidad,
      "project": $scope.finding.proyecto_fluid,
      "userMail": userEmail
    };
    const modalInstance = $uibModal.open({
      "animation": true,
      "backdrop": "static",
      "controller" ($scope, $uibModalInstance, mailData) {
        $scope.modalTitle = $translate.instant("search_findings." +
                                          "tab_description.verified_finding");
        $scope.ok = function ok () {
          // Consumir el servicio
          const req = projectFtry.findingVerified(mailData);
          // Capturar la Promisse
          req.then((response) => {
            if (!response.error) {
              // Tracking mixpanel
              const org = Organization.toUpperCase();
              const projt = descData.project.toUpperCase();
              mixPanelDashboard.trackFindingDetailed(
                "findingVerified",
                userName,
                userEmail,
                org,
                projt,
                descData.findingId
              );
              const updatedAt = $translate.instant("proj_alerts.updatedTitle");
              const updatedAc = $translate.instant("proj_alerts." +
                                                   "verified_success");
              $msg.success(updatedAc, updatedAt);
              $uibModalInstance.close();
              location.reload();
            }
            else if (response.error) {
              Rollbar.error("Error: An error occurred " +
                            "when verifying the finding");
              $msg.error($translate.instant("proj_alerts.error_textsad"));
            }
          });
        };
        $scope.close = function close () {
          $uibModalInstance.close();
        };
      },
      "resolve": {"mailData": descData},
      "templateUrl": `${BASE.url}assets/views/project/confirmMdl.html`
    });
  };
  $scope.goBack = function goBack () {
    $scope.view.project = true;
    $scope.view.finding = false;
    projectData = [];
    $state.go("ProjectFindings", {"project": $scope.project});
    $("html, body").animate(
      {"scrollTop": $scope.currentScrollPosition},
      "fast"
    );
  };
  $scope.urlDescription = function urlDescription () {
    location.replace(`${window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/description`);
  };
  $scope.urlSeverity = function urlSeverity () {
    location.replace(`${window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/severity`);
  };
  $scope.urlTracking = function urlTracking () {
    location.replace(`${window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/tracking`);
  };
  $scope.urlEvidence = function urlEvidence () {
    location.replace(`${window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/evidence`);
  };
  $scope.urlExploit = function urlExploit () {
    location.replace(`${window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/exploit`);
  };
  $scope.urlRecords = function urlRecords () {
    location.replace(`${window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/records`);
  };
  $scope.urlComments = function urlComments () {
    location.replace(`${window.location.href.split($stateParams.id)[0] +
                      $stateParams.id}/comments`);
  };
  $scope.activeTab = function activeTab (tabName, errorName, org, projt) {
    const tabNames = {
      "#comment": "#commentItem",
      "#cssv2": "#cssv2Item",
      "#evidence": "#evidenceItem",
      "#exploit": "#exploitItem",
      "#info": "#infoItem",
      "#records": "#recordsItem",
      "#tracking": "#trackingItem"
    };
    for (let inc = 0; inc < Object.keys(tabNames).length; inc++) {
      if (Object.keys(tabNames)[inc] === tabName) {
        $(tabName).addClass("active");
        $(tabNames[tabName]).addClass("active");
      }
      else {
        $(Object.keys(tabNames)[inc]).removeClass("active");
        $(tabNames[Object.keys(tabNames)[inc]]).removeClass("active");
      }
    }
    // Tracking mixpanel
    mixPanelDashboard.trackFindingDetailed(
      errorName,
      userName,
      userEmail,
      org,
      projt,
      $scope.finding.id
    );
  };
  $scope.urlEvents = function urlEvents () {
    $state.go("ProjectEvents", {"project": $stateParams.project});
  };
  $scope.init = function init () {
    const projectName = $stateParams.project;
    const findingId = $stateParams.finding;
    $scope.userRole = userRole;
    // Control para alternar los campos editables
    $scope.onlyReadableTab1 = true;
    $scope.onlyReadableTab2 = true;
    $scope.onlyReadableTab3 = true;
    $scope.onlyReadableTab4 = true;
    $scope.onlyReadableTab5 = true;
    $scope.onlyReadableTab6 = true;
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
    }
    // Inicializacion para consulta de hallazgos
    $scope.configColorPalette();
    $scope.finding = {};
    $scope.finding.id = $stateParams.id;
    $scope.loadFindingByID($stateParams.id);
    $scope.goUp();
    const org = Organization.toUpperCase();
    const projt = projectName.toUpperCase();
    $scope.alertHeader(org, projt);
    if (window.location.hash.indexOf("description") !== -1) {
      $scope.activeTab("#info", "FindingDescription", org, projt);
    }
    if (window.location.hash.indexOf("severity") !== -1) {
      $scope.activeTab("#cssv2", "FindingSeverity", org, projt);
    }
    if (window.location.hash.indexOf("tracking") !== -1) {
      $scope.activeTab("#tracking", "FindingTracking", org, projt);
    }
    if (window.location.hash.indexOf("evidence") !== -1) {
      $scope.activeTab("#evidence", "FindingEvidence", org, projt);
    }
    if (window.location.hash.indexOf("exploit") !== -1) {
      $scope.activeTab("#exploit", "FindingExploit", org, projt);
    }
    if (window.location.hash.indexOf("records") !== -1) {
      $scope.activeTab("#records", "FindingRecords", org, projt);
      const recordinfo = findingFtry.findingRecordsTab($scope, findingData);
      $scope.hasRecords = recordinfo[0];
      findingData.hasRecords = recordinfo[1];
    }
    if (window.location.hash.indexOf("comments") !== -1) {
      $scope.activeTab("#comment", "FindingComments", org, projt);
      findingFtry.findingCommentTab($scope, $stateParams);
    }
  };
  $scope.init();
});
