/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,0.4,0.6,1,1.176,1.5,2,3,4,5,6,6.9,7,9,10,10.41,20,50,80,100,200,500,1000,10000] }]*/
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams","$state","response"] }]*/
/* global
BASE, document, $, $msg, userName, integrates, userEmail, userName, Rollbar, mixPanelDashboard, userRole, findingType, actor,
scenario, authentication, confidenciality, Organization, resolutionLevel, explotability, availability, tratamiento, updateEvidencesFiles:true,
findingData:true, realiabilityLevel, updateEvidenceText:true, categories, probabilities, accessVector, integrity, accessComplexity, projectData:true
*/
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
  ngNotify, findingFactory, projectFtry
) {
  $scope.findingHeaderBuilding = function findingHeaderBuilding () {
    $scope.header = {};
    const cierres = $scope.finding.cierres;
    const cierresTmp = [];
    for (let cont = 0; cont < cierres.length; cont++) {
      const cierre = cierres[cont];
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
      $scope.header.findingValueDescription = $translate.instant("finding_formstack.criticity_header.high");
      $scope.header.findingValueColor = $scope.colors.critical;
    }
    else if (findingValue >= 4 && findingValue <= 6.9) {
      $scope.header.findingValueDescription = $translate.instant("finding_formstack.criticity_header.moderate");
      $scope.header.findingValueColor = $scope.colors.moderate;
    }
    else {
      $scope.header.findingValueDescription = $translate.instant("finding_formstack.criticity_header.tolerable");
      $scope.header.findingValueColor = $scope.colors.tolerable;
    }

    if ($scope.header.findingState === "Abierto" || $scope.header.findingState === "Open") {
      $scope.header.findingStateColor = $scope.colors.critical;
    }
    else if ($scope.header.findingState === "Parcialmente cerrado" || $scope.header.findingState === "Partially closed") {
      $scope.header.findingStateColor = $scope.colors.moderate;
    }
    else {
      $scope.header.findingStateColor = $scope.colors.ok;
    }

    $scope.header.findingCount = $scope.finding.cardinalidad;
    findingData.header = $scope.header;
  };
  String.prototype.replaceAll = function replaceAll (search, replace) { /* eslint no-extend-native: ["error", { "exceptions": ["String"] }]*/
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
          html += `<strong>Atención! </strong>${response.data[0].message}</div>`;
          document.getElementById("header_alert").innerHTML = html;
        }
      }
    });
  };
  $scope.findingExploitTab = function findingExploitTab () {
    $scope.hasExploit = false;
    findingData.hasExploit = $scope.hasExploit;
    let exploit = {};
    const req = projectFtry.getEvidences($scope.finding.id);
    req.then((response) => {
      if (!response.error) {
        if (response.data.length > 0) {
          /* eslint func-style: ["error", "expression"]*/
          const respFunction = function (response) {
            if (!response.error) {
              let responses = response.replaceAll("<", "&lt;");
              responses = response.replaceAll(">", "&gt;");
              $scope.exploitURL = responses;
              findingData.exploitURL = $scope.exploitURL;
            }
            else if (response.error) {
              Rollbar.error("Error: An error occurred loading exploit from S3");
            }
          };
          for (let cont = 0; cont < response.data.length; cont++) {
            if (typeof response.data[cont].exploit !== "undefined" &&
                            response.data[cont].es_exploit === true &&
                              $scope.finding.cierres.length === 0) {
              exploit = projectFtry.getExploit($scope.finding.id, response.data[cont].exploit);
              $scope.hasExploit = true;
              findingData.hasExploit = $scope.hasExploit;
              exploit.then((response) => {
                respFunction(response);
              });
            }
            else if (typeof $scope.finding.exploit !== "undefined" && $scope.finding.cierres.length === 0) {
              exploit = projectFtry.getExploit($scope.finding.id, $scope.finding.exploit);
              $scope.hasExploit = true;
              findingData.hasExploit = $scope.hasExploit;
              exploit.then((response) => {
                respFunction(response);
              });
            }
            else {
              $scope.hasExploit = false;
              findingData.hasExploit = $scope.hasExploit;
            }
          }
        }
        else if (typeof $scope.finding.exploit !== "undefined" && $scope.finding.cierres.length === 0) {
          exploit = projectFtry.getExploit($scope.finding.id, $scope.finding.exploit);
          $scope.hasExploit = true;
          findingData.hasExploit = $scope.hasExploit;
          exploit.then((response) => {
            if (!response.error) {
              let responses = response.replaceAll("<", "&lt;");
              responses = response.replaceAll(">", "&gt;");
              $scope.exploitURL = responses;
              findingData.exploitURL = $scope.exploitURL;
            }
            else if (response.error) {
              Rollbar.error("Error: An error occurred loading exploit");
            }
          });
        }
        else {
          $scope.hasExploit = false;
          findingData.hasExploit = $scope.hasExploit;
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
          fileName = (input.getAttribute("data-multiple-caption") || "").replace("{count}", input.files.length);
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
        "name": $translate.instant("search_findings.tab_evidence.animation_exploit"),
        "ref": 0
      });
    }
    if (refList.indexOf(1) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": $translate.instant("search_findings.tab_evidence.evidence_exploit"),
        "ref": 1
      });
    }
    if (refList.indexOf(2) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 1`,
        "ref": 2
      });
    }
    if (refList.indexOf(3) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 2`,
        "ref": 3
      });
    }
    if (refList.indexOf(4) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 3`,
        "ref": 4
      });
    }
    if (refList.indexOf(5) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 4`,
        "ref": 5
      });
    }
    if (refList.indexOf(6) === -1) {
      $scope.tabEvidences.push({
        "desc": "",
        "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 5`,
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
          fileName = (input.getAttribute("data-multiple-caption") || "").replace("{count}", input.files.length);
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
          fileName = (input.getAttribute("data-multiple-caption") || "").replace("{count}", input.files.length);
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
          const req = projectFtry.UpdateCSSv2(updateData);
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
    data.append("url", `${$stateParams.project.toLowerCase()}-${$scope.finding.id}`);
    data.append("findingId", $scope.finding.id);
    data.append("document", fileInput.files[0]);
    const fileName = fileInput.files[0].name;
    const dots = fileName.split(".");
    const fileType = `.${dots[dots.length - 1]}`;
    const pngMaxSize = 2097152;
    const gifMaxSize = 10485760;
    const pyMaxSize = 1048576;
    const csvMaxSize = 1048576;
    if ((fileType === ".png" || fileType === ".PNG") && fileInput.files[0].size > pngMaxSize) {
      errorAc1 = $translate.instant("proj_alerts.file_size_png");
      $msg.error(errorAc1);
      return false;
    }
    if ((fileType === ".gif" || fileType === ".GIF") && fileInput.files[0].size > gifMaxSize) {
      errorAc1 = $translate.instant("proj_alerts.file_size");
      $msg.error(errorAc1);
      return false;
    }
    if ((fileType === ".py" || fileType === ".PY") && fileInput.files[0].size > pyMaxSize) {
      errorAc1 = $translate.instant("proj_alerts.file_size_py");
      $msg.error(errorAc1);
      return false;
    }
    if ((fileType === ".csv" || fileType === ".CSV") && fileInput.files[0].size > csvMaxSize) {
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
    else if (evImages.indexOf(evImage) !== -1 && (fileType !== ".png" && fileType !== ".PNG")) {
      errorAc1 = $translate.instant("proj_alerts.file_type_png");
      $msg.error(errorAc1);
      return false;
    }
    const responseFunction = function (response) {
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
    const errorFunction = function (response) {
      if (!response.error) {
        errorAc1 = $translate.instant("proj_alerts.no_file_update");
        Rollbar.error("Error: An error occurred updating evidences");
        $msg.error(errorAc1);
        return false;
      }
    };
    projectFtry.UpdateEvidenceFiles(data, responseFunction, errorFunction);
  };
  updateEvidenceText = function (element) {
    const evImage = $(element).attr("target");
    const data = {};
    data.id = $scope.finding.id;
    const description = $(`#evidenceText${evImage}`).val();
    const file = $(`#evidence${evImage}`).val();
    if (description === "" || $scope.evidenceDescription[evImage] === description) {
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
      const req = projectFtry.UpdateEvidenceText(data);
      // Capturar la Promisse
      req.then((response) => {
        if (!response.error) {
          const updatedAt = $translate.instant("proj_alerts.updatedTitle");
          const updatedAc = $translate.instant("proj_alerts.updated_cont_description");
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
        Rollbar.error("Error: An error occurred updating evidences description");
        $msg.error(errorAc1);
        return false;
      });
    }
  };
  $scope.deleteFinding = function deleteFinding () {
    // Obtener datos
    const descData = {"id": $scope.finding.id};
    const modalInstance = $uibModal.open({
      "animation": true,
      "backdrop": "static",
      "controller" ($scope, $uibModalInstance, updateData, $stateParams, $state) {
        $scope.vuln = {};
        $scope.modalTitle = $translate.instant("confirmmodal.title_finding");
        $scope.ok = function ok () {
          $scope.vuln.id = updateData.id;
          // Consumir el servicio
          const req = projectFtry.DeleteFinding($scope.vuln);
          // Capturar la Promisse
          req.then((response) => {
            if (!response.error) {
              const updatedAt = $translate.instant("proj_alerts.updatedTitle");
              const updatedAc = $translate.instant("proj_alerts.updated_cont");
              $msg.success(updatedAc, updatedAt);
              $uibModalInstance.close();
              $state.go("ProjectFindings", {"project": $stateParams.project});
              // Tracking mixpanel
              mixPanelDashboard.trackFinding("DeleteFinding", userEmail, descData.id);
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
      if (element.indexOf("https://") !== -1 || element.indexOf("http://") !== -1) {
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
    if (!$scope.isEmpty(findingData) && findingData.data.proyecto_fluid.toLowerCase() === $stateParams.project.toLowerCase() &&
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
      const req = findingFactory.getVulnById(id);
      req.then((response) => {
        if (!response.error && $stateParams.project === response.data.proyecto_fluid.toLowerCase()) {
          findingData.data = response.data;
          $scope.finding = response.data;
          $scope.loadFindingContent();
          $scope.findingHeaderBuilding();
          $scope.remediatedView();
          findingData.remediated = $scope.isRemediated;
          $scope.view.project = false;
          $scope.view.finding = true;
          $scope.findingEvidenceTab();
          $scope.findingExploitTab();
          $scope.findingRecordsTab();
          $scope.findingCommentTab();
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
          return false;
        }
      });
    }
  };
  $scope.loadFindingContent = function loadFindingContent () {
    $scope.aux = {};
    $scope.aux.tratamiento = $scope.finding.tratamiento;
    $scope.aux.razon = $scope.finding.razonTratamiento;
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
    if ($scope.finding.suscripcion === "Continua" || $scope.finding.suscripcion === "Concurrente" || $scope.finding.suscripcion === "Si") {
      $scope.isContinuous = true;
    }
    else {
      $scope.isContinuous = false;
    }
    if ($scope.finding.suscripcion !== "Concurrente" && $scope.finding.suscripcion !== "Puntual" && $scope.finding.suscripcion !== "Continua") {
      Rollbar.warning(`Warning: Finding ${$scope.finding.id} without type`);
    }
    $scope.aux.responsable = $scope.finding.responsableTratamiento;
    $scope.aux.bts = $scope.finding.btsExterno;
    $scope.finding.hasUrl = $scope.hasUrl($scope.finding.btsExterno);
    $scope.finding.cweIsUrl = $scope.hasUrl($scope.finding.cwe);
    switch ($scope.finding.actor) {
    case "​Cualquier persona en Internet":
      $scope.finding.actor = $translate.instant("finding_formstack.actor.any_internet");
      break;
    case "Cualquier cliente de la organización":
      $scope.finding.actor = $translate.instant("finding_formstack.actor.any_costumer");
      break;
    case "Solo algunos clientes de la organización":
      $scope.finding.actor = $translate.instant("finding_formstack.actor.some_costumer");
      break;
    case "Cualquier persona con acceso a la estación":
      $scope.finding.actor = $translate.instant("finding_formstack.actor.any_access");
      break;
    case "Cualquier empleado de la organización":
      $scope.finding.actor = $translate.instant("finding_formstack.actor.any_employee");
      break;
    case "Solo algunos empleados":
      $scope.finding.actor = $translate.instant("finding_formstack.actor.some_employee");
      break;
    case "Solo un empleado":
      $scope.finding.actor = $translate.instant("finding_formstack.actor.one_employee");
      break;
    default:
      $scope.finding.actor = $scope.finding.actor;
    }
    switch ($scope.finding.autenticacion) {
    case "0.704 | Ninguna: No se requiere autenticación":
      $scope.finding.autenticacion = $translate.instant("finding_formstack.authentication.any_authen");
      break;
    case "0.560 | Única: Único punto de autenticación":
      $scope.finding.autenticacion = $translate.instant("finding_formstack.authentication.single_authen");
      break;
    case "0.450 | Multiple: Multiples puntos de autenticación":
      $scope.finding.autenticacion = $translate.instant("finding_formstack.authentication.multiple_authen");
      break;
    default:
      $scope.finding.autenticacion = $scope.finding.autenticacion;
    }
    switch ($scope.finding.categoria) {
    case "Actualizar y configurar las líneas base de seguridad de los componentes":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.update_base");
      break;
    case "Definir el modelo de autorización considerando el principio de mínimo privilegio":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.define_model");
      break;
    case "Desempeño":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.performance");
      break;
    case "Eventualidad":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.event");
      break;
    case "Evitar exponer la información técnica de la aplicación, servidores y plataformas":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.avoid_technical");
      break;
    case "Excluir datos sensibles del código fuente y del registro de eventos":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.exclude_finding");
      break;
    case "Fortalecer controles en autenticación y manejo de sesión":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.strengt_authen");
      break;
    case "Fortalecer controles en el procesamiento de archivos":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.strengt_process");
      break;
    case "Fortalecer la protección de datos almacenados relacionados con contraseñas o llaves criptográficas":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.strengt_protect");
      break;
    case "Implementar controles para validar datos de entrada":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.validate_input");
      break;
    case "Mantenibilidad":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.maintain");
      break;
    case "Registrar eventos para trazabilidad y auditoría":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.record_event");
      break;
    case "Utilizar protocolos de comunicación seguros":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.secure_protoc");
      break;
    case "Validar la integridad de las transacciones en peticiones HTTP":
      $scope.finding.categoria = $translate.instant("finding_formstack.category.validate_http");
      break;
    default:
      $scope.finding.categoria = $scope.finding.categoria;
    }
    switch ($scope.finding.complejidadAcceso) {
    case "0.350 | Alto: Se requieren condiciones especiales como acceso administrativo":
      $scope.finding.complejidadAcceso = $translate.instant("finding_formstack.complexity.high_complex");
      break;
    case "0.610 | Medio: Se requieren algunas condiciones como acceso al sistema":
      $scope.finding.complejidadAcceso = $translate.instant("finding_formstack.complexity.medium_complex");
      break;
    case "0.710 | Bajo: No se requiere ninguna condición especial":
      $scope.finding.complejidadAcceso = $translate.instant("finding_formstack.complexity.low_complex");
      break;
    default:
      $scope.finding.complejidadAcceso = $scope.finding.complejidadAcceso;
    }
    switch ($scope.finding.escenario) {
    case "Anónimo desde Internet":
      $scope.finding.escenario = $translate.instant("finding_formstack.scenario.anon_inter");
      break;
    case "Anónimo desde Intranet":
      $scope.finding.escenario = $translate.instant("finding_formstack.scenario.anon_intra");
      break;
    case "Escaneo de Infraestructura":
      $scope.finding.escenario = $translate.instant("finding_formstack.scenario.infra_scan");
      break;
    case "Extranet usuario no autorizado":
      $scope.finding.escenario = $translate.instant("finding_formstack.scenario.unauth_extra");
      break;
    case "Internet usuario autorizado":
      $scope.finding.escenario = $translate.instant("finding_formstack.scenario.auth_inter");
      break;
    case "Internet usuario no autorizado":
      $scope.finding.escenario = $translate.instant("finding_formstack.scenario.unauth_inter");
      break;
    case "Intranet usuario autorizado":
      $scope.finding.escenario = $translate.instant("finding_formstack.scenario.auth_intra");
      break;
    case "Intranet usuario no autorizado":
      $scope.finding.escenario = $translate.instant("finding_formstack.scenario.unauth_inter");
      break;
    default:
      $scope.finding.escenario = $scope.finding.escenario;
    }
    switch ($scope.finding.estado) {
    case "Abierto":
      $scope.finding.estado = $translate.instant("finding_formstack.status.open");
      break;
    case "Cerrado":
      $scope.finding.estado = $translate.instant("finding_formstack.status.close");
      break;
    case "Parcialmente cerrado":
      $scope.finding.estado = $translate.instant("finding_formstack.status.part_close");
      break;
    default:
      $scope.finding.estado = $scope.finding.estado;
    }
    switch ($scope.finding.explotabilidad) {
    case "0.850 | Improbable: No existe un exploit":
      $scope.finding.explotabilidad = $translate.instant("finding_formstack.exploitability.improbable");
      break;
    case "0.900 | Conceptual: Existen pruebas de laboratorio":
      $scope.finding.explotabilidad = $translate.instant("finding_formstack.exploitability.conceptual");
      break;
    case "0.950 | Funcional: Existe exploit":
      $scope.finding.explotabilidad = $translate.instant("finding_formstack.exploitability.functional");
      break;
    case "1.000 | Alta: No se requiere exploit o se puede automatizar":
      $scope.finding.explotabilidad = $translate.instant("finding_formstack.exploitability.high");
      break;
    default:
      $scope.finding.explotabilidad = $scope.finding.explotabilidad;
    }
    switch ($scope.finding.explotable) {
    case "Si":
      $scope.finding.explotable = $translate.instant("finding_formstack.exploitable.yes");
      break;
    case "No":
      $scope.finding.explotable = $translate.instant("finding_formstack.exploitable.no");
      break;
    default:
      $scope.finding.explotable = $scope.finding.explotable;
    }
    switch ($scope.finding.impactoConfidencialidad) {
    case "0 | Ninguno: No se presenta ningún impacto":
      $scope.finding.impactoConfidencialidad = $translate.instant("finding_formstack.confidenciality.none");
      break;
    case "0.275 | Parcial: Se obtiene acceso a la información pero no control sobre ella":
      $scope.finding.impactoConfidencialidad = $translate.instant("finding_formstack.confidenciality.partial");
      break;
    case "0.660 | Completo: Se controla toda la información relacionada con el objetivo":
      $scope.finding.impactoConfidencialidad = $translate.instant("finding_formstack.confidenciality.complete");
      break;
    default:
      $scope.finding.impactoConfidencialidad = $scope.finding.impactoConfidencialidad;
    }
    switch ($scope.finding.impactoDisponibilidad) {
    case "0 | Ninguno: No se presenta ningún impacto":
      $scope.finding.impactoDisponibilidad = $translate.instant("finding_formstack.availability.none");
      break;
    case "0.275 | Parcial: Se presenta intermitencia en el acceso al objetivo":
      $scope.finding.impactoDisponibilidad = $translate.instant("finding_formstack.availability.partial");
      break;
    case "0.660 | Completo: Hay una caída total del objetivo":
      $scope.finding.impactoDisponibilidad = $translate.instant("finding_formstack.availability.complete");
      break;
    default:
      $scope.finding.impactoDisponibilidad = $scope.finding.impactoDisponibilidad;
    }
    switch ($scope.finding.impactoIntegridad) {
    case "0 | Ninguno: No se presenta ningún impacto":
      $scope.finding.impactoIntegridad = $translate.instant("finding_formstack.integrity.none");
      break;
    case "0.275 | Parcial: Es posible modificar cierta información del objetivo":
      $scope.finding.impactoIntegridad = $translate.instant("finding_formstack.integrity.partial");
      break;
    case "0.660 | Completo: Es posible modificar toda la información del objetivo":
      $scope.finding.impactoIntegridad = $translate.instant("finding_formstack.integrity.complete");
      break;
    default:
      $scope.finding.impactoIntegridad = $scope.finding.impactoIntegridad;
    }
    switch ($scope.finding.nivelConfianza) {
    case "0.900 | No confirmado: Existen pocas fuentes que reconocen la vulnerabilidad":
      $scope.finding.nivelConfianza = $translate.instant("finding_formstack.confidence.not_confirm");
      break;
    case "0.950 | No corroborado: La vulnerabilidad es reconocida por fuentes no oficiales":
      $scope.finding.nivelConfianza = $translate.instant("finding_formstack.confidence.not_corrob");
      break;
    case "1.000 | Confirmado: La vulnerabilidad es reconocida por el fabricante":
      $scope.finding.nivelConfianza = $translate.instant("finding_formstack.confidence.confirmed");
      break;
    default:
      $scope.finding.nivelConfianza = $scope.finding.nivelConfianza;
    }
    switch ($scope.finding.nivelResolucion) {
    case "0.950 | Paliativa: Existe un parche que no fue publicado por el fabricante":
      $scope.finding.nivelResolucion = $translate.instant("finding_formstack.resolution.palliative");
      break;
    case "0.870 | Oficial: Existe un parche disponible por el fabricante":
      $scope.finding.nivelResolucion = $translate.instant("finding_formstack.resolution.official");
      break;
    case "0.900 | Temporal: Existen soluciones temporales":
      $scope.finding.nivelResolucion = $translate.instant("finding_formstack.resolution.temporal");
      break;
    case "1.000 | Inexistente: No existe solución":
      $scope.finding.nivelResolucion = $translate.instant("finding_formstack.resolution.non_existent");
      break;
    default:
      $scope.finding.nivelResolucion = $scope.finding.nivelResolucion;
    }
    switch ($scope.finding.probabilidad) {
    case "100% Vulnerado Anteriormente":
      $scope.finding.probabilidad = $translate.instant("finding_formstack.probability.prev_vuln");
      break;
    case "75% Fácil de vulnerar":
      $scope.finding.probabilidad = $translate.instant("finding_formstack.probability.easy_vuln");
      break;
    case "50% Posible de vulnerar":
      $scope.finding.probabilidad = $translate.instant("finding_formstack.probability.possible_vuln");
      break;
    case "25% Difícil de vulnerar":
      $scope.finding.probabilidad = $translate.instant("finding_formstack.probability.diffic_vuln");
      break;
    default:
      $scope.finding.probabilidad = $scope.finding.probabilidad;
    }
    switch ($scope.finding.tipoHallazgoCliente) {
    case "Higiene":
      $scope.finding.tipoHallazgoCliente = $translate.instant("finding_formstack.findingType.hygiene");
      break;
    case "Vulnerabilidad":
      $scope.finding.tipoHallazgoCliente = $translate.instant("finding_formstack.findingType.vuln");
      break;
    default:
      $scope.finding.tipoHallazgoCliente = $scope.finding.tipoHallazgoCliente;
    }
    switch ($scope.finding.tipo_prueba) {
    case "Análisis":
      $scope.finding.tipoPrueba = $translate.instant("finding_formstack.test_method.analysis");
      break;
    case "Aplicación":
      $scope.finding.tipoPrueba = $translate.instant("finding_formstack.test_method.app");
      break;
    case "Binario":
      $scope.finding.tipoPrueba = $translate.instant("finding_formstack.test_method.binary");
      break;
    case "Código":
      $scope.finding.tipoPrueba = $translate.instant("finding_formstack.test_method.code");
      break;
    case "Infraestructura":
      $scope.finding.tipoPrueba = $translate.instant("finding_formstack.test_method.infras");
      break;
    default:
      $scope.finding.tipoPrueba = $scope.finding.tipoPrueba;
    }
    switch ($scope.finding.vectorAcceso) {
    case "0.646 | Red adyacente: Explotable desde el mismo segmento de red":
      $scope.finding.vectorAcceso = $translate.instant("finding_formstack.access_vector.adjacent");
      break;
    case "1.000 | Red: Explotable desde Internet":
      $scope.finding.vectorAcceso = $translate.instant("finding_formstack.access_vector.network");
      break;
    case "0.395 | Local: Explotable con acceso local al objetivo":
      $scope.finding.vectorAcceso = $translate.instant("finding_formstack.access_vector.local");
      break;
    default:
      $scope.finding.vectorAcceso = $scope.finding.vectorAcceso;
    }
    switch ($scope.finding.tratamiento) {
    case "Asumido":
      $scope.finding.tratamiento = $translate.instant("finding_formstack.treatment_header.asummed");
      break;
    case "Nuevo":
      $scope.finding.tratamiento = $translate.instant("finding_formstack.treatment_header.working");
      break;
    case "Remediar":
      $scope.finding.tratamiento = $translate.instant("finding_formstack.treatment_header.remediated");
      break;
    case "Resuelto":
      $scope.finding.tratamiento = $translate.instant("finding_formstack.treatment_header.resolved");
      break;
    default:
      $scope.finding.tratamiento = $scope.finding.tratamiento;
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
    if (!$scope.isManager && !$scope.isAssumed && !$scope.isClosed && $scope.isContinuous) {
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
        "tError": "<a href=\"%url%\">The image #%curr%</a> could not be loaded.",
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
    const ImpCon = parseFloat($scope.finding.impacto_confidencialidad.split(" | ")[0]);
    const ImpInt = parseFloat($scope.finding.impacto_integridad.split(" | ")[0]);
    const ImpDis = parseFloat($scope.finding.impacto_disponibilidad.split(" | ")[0]);
    const AccCom = parseFloat($scope.finding.complejidad_acceso.split(" | ")[0]);
    const AccVec = parseFloat($scope.finding.vector_acceso.split(" | ")[0]);
    const Auth = parseFloat($scope.finding.autenticacion.split(" | ")[0]);
    const Explo = parseFloat($scope.finding.explotabilidad.split(" | ")[0]);
    const Resol = parseFloat($scope.finding.nivel_resolucion.split(" | ")[0]);
    const Confi = parseFloat($scope.finding.nivel_confianza.split(" | ")[0]);
    const BaseScore = ((0.6 * 10.41 * (1 - ((1 - ImpCon) * (1 - ImpInt) * (1 - ImpDis)))) + (0.4 * 20 * AccCom * Auth * AccVec) - 1.5) * 1.176;
    const Temporal = BaseScore * Explo * Resol * Confi;
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
  $scope.findingEvidenceTab = function findingEvidenceTab () {
    $scope.tabEvidences = [];
    let url = "";
    const evidenceList = [];
    const urlPre = `${window.location.href.split("dashboard#!/")[0] + window.location.href.split("dashboard#!/")[1]}/`;
    const req = projectFtry.getEvidences($scope.finding.id);
    req.then((response) => {
      if (!response.error) {
        if (response.data.length > 0) {
          for (let cont = 0; cont < response.data.length; cont++) {
            if (typeof response.data[cont].animacion !== "undefined" && response.data[cont].es_animacion === true) {
              url = urlPre + response.data[cont].animacion;
              evidenceList.push({
                "desc": $translate.instant("search_findings.tab_evidence.animation_exploit"),
                "name": $translate.instant("search_findings.tab_evidence.animation_exploit"),
                "ref": 0,
                url
              });
            }
            else if (typeof $scope.finding.animacion !== "undefined") {
              url = urlPre + $scope.finding.animacion;
              evidenceList.push({
                "desc": $translate.instant("search_findings.tab_evidence.animation_exploit"),
                "name": $translate.instant("search_findings.tab_evidence.animation_exploit"),
                "ref": 0,
                url
              });
            }
            if (typeof response.data[cont].explotacion !== "undefined" && response.data[cont].es_explotacion === true) {
              url = urlPre + response.data[cont].explotacion;
              evidenceList.push({
                "desc": $translate.instant("search_findings.tab_evidence.evidence_exploit"),
                "name": $translate.instant("search_findings.tab_evidence.evidence_exploit"),
                "ref": 1,
                url
              });
            }
            else if (typeof $scope.finding.explotacion !== "undefined") {
              url = urlPre + $scope.finding.explotacion;
              evidenceList.push({
                "desc": $translate.instant("search_findings.tab_evidence.evidence_exploit"),
                "name": $translate.instant("search_findings.tab_evidence.evidence_exploit"),
                "ref": 1,
                url
              });
            }
            if (typeof $scope.finding.desc_evidencia_1 !== "undefined" &&
                          typeof response.data[cont].ruta_evidencia_1 !== "undefined" &&
                            response.data[cont].es_ruta_evidencia_1 === true) {
              url = urlPre + response.data[cont].ruta_evidencia_1;
              evidenceList.push({
                "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_1),
                "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 1`,
                "ref": 2,
                url
              });
            }
            else if (typeof $scope.finding.desc_evidencia_1 !== "undefined" &&
                          typeof $scope.finding.ruta_evidencia_1 !== "undefined") {
              url = urlPre + $scope.finding.ruta_evidencia_1;
              evidenceList.push({
                "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_1),
                "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 1`,
                "ref": 2,
                url
              });
            }
            if (typeof $scope.finding.desc_evidencia_2 !== "undefined" &&
                          typeof response.data[cont].ruta_evidencia_2 !== "undefined" &&
                            response.data[cont].es_ruta_evidencia_2 === true) {
              url = urlPre + response.data[cont].ruta_evidencia_2;
              evidenceList.push({
                "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_2),
                "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 2`,
                "ref": 3,
                url
              });
            }
            else if (typeof $scope.finding.desc_evidencia_2 !== "undefined" &&
                          typeof $scope.finding.ruta_evidencia_2 !== "undefined") {
              url = urlPre + $scope.finding.ruta_evidencia_2;
              evidenceList.push({
                "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_2),
                "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 2`,
                "ref": 3,
                url
              });
            }
            if (typeof $scope.finding.desc_evidencia_3 !== "undefined" &&
                          typeof response.data[cont].ruta_evidencia_3 !== "undefined" &&
                            response.data[cont].es_ruta_evidencia_3 === true) {
              url = urlPre + response.data[cont].ruta_evidencia_3;
              evidenceList.push({
                "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_3),
                "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 3`,
                "ref": 4,
                url
              });
            }
            else if (typeof $scope.finding.desc_evidencia_3 !== "undefined" &&
                          typeof $scope.finding.ruta_evidencia_3 !== "undefined") {
              url = urlPre + $scope.finding.ruta_evidencia_3;
              evidenceList.push({
                "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_3),
                "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 3`,
                "ref": 4,
                url
              });
            }
            if (typeof $scope.finding.desc_evidencia_4 !== "undefined" &&
                          typeof response.data[cont].ruta_evidencia_4 !== "undefined" &&
                            response.data[cont].es_ruta_evidencia_4 === true) {
              url = urlPre + response.data[cont].ruta_evidencia_4;
              evidenceList.push({
                "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_4),
                "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 4`,
                "ref": 5,
                url
              });
            }
            else if (typeof $scope.finding.desc_evidencia_4 !== "undefined" &&
                          typeof $scope.finding.ruta_evidencia_4 !== "undefined") {
              url = urlPre + $scope.finding.ruta_evidencia_4;
              evidenceList.push({
                "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_4),
                "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 4`,
                "ref": 5,
                url
              });
            }
            if (typeof $scope.finding.desc_evidencia_5 !== "undefined" &&
                          typeof response.data[cont].ruta_evidencia_5 !== "undefined" &&
                            response.data[cont].es_ruta_evidencia_5 === true) {
              url = urlPre + response.data[cont].ruta_evidencia_5;
              evidenceList.push({
                "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_5),
                "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 5`,
                "ref": 6,
                url
              });
            }
            else if (typeof $scope.finding.desc_evidencia_5 !== "undefined" &&
                          typeof $scope.finding.ruta_evidencia_5 !== "undefined") {
              url = urlPre + $scope.finding.ruta_evidencia_5;
              evidenceList.push({
                "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_5),
                "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 5`,
                "ref": 6,
                url
              });
            }
            $scope.tabEvidences = evidenceList;
            findingData.tabEvidences = evidenceList;
          }
        }
        else {
          if (typeof $scope.finding.animacion !== "undefined") {
            url = urlPre + $scope.finding.animacion;
            evidenceList.push({
              "desc": $translate.instant("search_findings.tab_evidence.animation_exploit"),
              "name": $translate.instant("search_findings.tab_evidence.animation_exploit"),
              "ref": 0,
              url
            });
          }
          if (typeof $scope.finding.explotacion !== "undefined") {
            url = urlPre + $scope.finding.explotacion;
            evidenceList.push({
              "desc": $translate.instant("search_findings.tab_evidence.evidence_exploit"),
              "name": $translate.instant("search_findings.tab_evidence.evidence_exploit"),
              "ref": 1,
              url
            });
          }
          if (typeof $scope.finding.desc_evidencia_1 !== "undefined" &&
                        typeof $scope.finding.ruta_evidencia_1 !== "undefined") {
            url = urlPre + $scope.finding.ruta_evidencia_1;
            evidenceList.push({
              "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_1),
              "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 1`,
              "ref": 2,
              url
            });
          }
          if (typeof $scope.finding.desc_evidencia_2 !== "undefined" &&
                        typeof $scope.finding.ruta_evidencia_2 !== "undefined") {
            url = urlPre + $scope.finding.ruta_evidencia_2;
            evidenceList.push({
              "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_2),
              "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 2`,
              "ref": 3,
              url
            });
          }
          if (typeof $scope.finding.desc_evidencia_3 !== "undefined" &&
                        typeof $scope.finding.ruta_evidencia_3 !== "undefined") {
            url = urlPre + $scope.finding.ruta_evidencia_3;
            evidenceList.push({
              "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_3),
              "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 3`,
              "ref": 4,
              url
            });
          }
          if (typeof $scope.finding.desc_evidencia_4 !== "undefined" &&
                        typeof $scope.finding.ruta_evidencia_4 !== "undefined") {
            url = urlPre + $scope.finding.ruta_evidencia_4;
            evidenceList.push({
              "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_4),
              "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 4`,
              "ref": 5,
              url
            });
          }
          if (typeof $scope.finding.desc_evidencia_5 !== "undefined" &&
                        typeof $scope.finding.ruta_evidencia_5 !== "undefined") {
            url = urlPre + $scope.finding.ruta_evidencia_5;
            evidenceList.push({
              "desc": $scope.capitalizeFirstLetter($scope.finding.desc_evidencia_5),
              "name": `${$translate.instant("search_findings.tab_evidence.evidence_name")} 5`,
              "ref": 6,
              url
            });
          }
          $scope.tabEvidences = evidenceList;
          findingData.tabEvidences = evidenceList;
        }
      }
      else if (response.error) {
        Rollbar.error("Error: An error occurred loading evidences");
        findingData.tabEvidences = evidenceList;
      }
    });
  };
  $scope.findingCommentTab = function findingCommentTab () {
    if (typeof $scope.finding.id !== "undefined") {
      const comments = projectFtry.getComments($scope.finding.id);
      comments.then((response) => {
        if (!response.error) {
          const usersArray = [];
          for (let cont = 0; cont < response.data.length; cont++) {
            const user = {
              "email": "",
              "fullname": ""
            };
            user.fullname = response.data[cont].fullname;
            user.email = response.data[cont].email;
            usersArray.push(user);
          }
          const saveComment = function saveComment (data) {
            // Convert pings to human readable format
            $(data.pings).each((index, id) => {
              const userInfo = usersArray.filter((user) => userInfo.id === id)[0];
              data.content = data.content.replace(`@${id}`, `@${userInfo.fullname}`);
            });
            return data;
          };
          $("#comments-container").comments({
            "enableAttachments": false,
            "enableEditing": false,
            "enableHashtags": true,
            "enablePinging": false,
            "enableUpvoting": false,
            "getComments" (success, error) {
              setTimeout(() => {
                success(response.data);
              }, 500);
            },
            "getUsers" (success, error) {
              setTimeout(() => {
                success(usersArray);
              }, 500);
            },
            "postComment" (data, success, error) {
              data.id = parseInt(Math.round(new Date() / 1000).toString() + (Math.random() * 10000).toString(9), 10);
              data.findingName = $scope.finding.hallazgo;
              data.project = $scope.finding.proyecto_fluid;
              data.findingUrl = window.location.href;
              data.remediated = false;
              const comment = projectFtry.addComment($scope.finding.id, data);
              comment.then((response) => {
                if (!response.error) {
                  // Tracking mixpanel
                  const org = Organization.toUpperCase();
                  const projt = $stateParams.project.toUpperCase();
                  mixPanelDashboard.trackFindingDetailed("FindingNewComment", userName, userEmail, org, projt, $scope.finding.id);
                  setTimeout(() => {
                    success(data);
                  }, 500);
                }
                else if (response.error) {
                  Rollbar.error("Error: An error occurred adding comment");
                }
              });
            },
            "roundProfilePictures": true,
            "textareaRows": 2
          });
        }
      });
    }
  };
  $scope.findingRecordsTab = function findingRecordsTab () {
    $scope.hasRecords = false;
    findingData.hasRecords = $scope.hasRecords;
    let vlang = "en-US";
    let record = {};
    const req = projectFtry.getEvidences($scope.finding.id);
    req.then((response) => {
      if (!response.error) {
        if (localStorage.lang === "en") {
          vlang = "en-US";
        }
        else {
          vlang = "es-CO";
        }
        if (response.data.length > 0) {
          const respFunction = function respFunction (response) {
            if (!response.error) {
              const dataCols = [];
              for (const cont in response.data[0]) {
                if ({}.hasOwnProperty.call(response.data[0], cont)) {
                  dataCols.push({
                    "field": cont,
                    "title": cont
                  });
                }
              }
              $("#recordsTable").bootstrapTable("destroy");
              $("#recordsTable").bootstrapTable({
                "columns": dataCols,
                "cookie": true,
                "cookieIdTable": "recordsTableCookie",
                "data": response.data,
                "locale": vlang
              });
              $("#recordsTable").bootstrapTable("refresh");
            }
            else if (response.error) {
              Rollbar.error("Error: An error occurred loading record from S3");
              const errorAc1 = $translate.instant("proj_alerts.error_textsad");
              $msg.error(errorAc1);
            }
          };
          for (let cont = 0; cont < response.data.length; cont++) {
            if (typeof response.data[cont].registros_archivo !== "undefined" &&
                            response.data[cont].es_registros_archivo === true) {
              record = projectFtry.getRecords($scope.finding.id, response.data[cont].registros_archivo);
              $scope.hasRecords = true;
              findingData.hasRecords = $scope.hasRecords;
              record.then((response) => {
                respFunction(response);
              });
            }
            else if (typeof $scope.finding.registros_archivo !== "undefined") {
              record = projectFtry.getRecords($scope.finding.id, $scope.finding.registros_archivo);
              $scope.hasRecords = true;
              findingData.hasRecords = $scope.hasRecords;
              record.then((response) => {
                respFunction(response);
              });
            }
            else if ((typeof $scope.finding.registros_archivo === "undefined" || typeof response.data[cont].registros_archivo === "undefined") &&
                            response.data[cont].es_registros_archivo === false) {
              $scope.hasRecords = false;
              findingData.hasRecords = $scope.hasRecords;
            }
          }
        }
        else if (typeof $scope.finding.registros_archivo !== "undefined") {
          record = projectFtry.getRecords($scope.finding.id, $scope.finding.registros_archivo);
          $scope.hasRecords = true;
          record.then((response) => {
            if (!response.error) {
              const dataCols = [];
              for (const cont in response.data[0]) {
                if ({}.hasOwnProperty.call(response.data[0], cont)) {
                  dataCols.push({
                    "field": cont,
                    "title": cont
                  });
                }
              }
              $("#recordsTable").bootstrapTable("destroy");
              $("#recordsTable").bootstrapTable({
                "columns": dataCols,
                "cookie": true,
                "cookieIdTable": "recordsTableCookie",
                "data": response.data,
                "locale": vlang
              });
              $("#recordsTable").bootstrapTable("refresh");
            }
            else if (response.error) {
              Rollbar.error("Error: An error occurred loading record");
              const errorAc1 = $translate.instant("proj_alerts.error_textsad");
              $msg.error(errorAc1);
            }
          });
        }
        else if (response.data.length <= 0 || typeof $scope.finding.registros_archivo === "undefined") {
          $scope.hasRecords = false;
          findingData.hasRecords = $scope.hasRecords;
        }
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
          $scope.finding.valorRiesgo = "(:r) Critico".replace(":r", vRiesgo.toFixed(1));
        }
        else if (vRiesgo >= 2 && vRiesgo < 3) {
          $scope.finding.valorRiesgo = "(:r) Moderado".replace(":r", vRiesgo.toFixed(1));
        }
        else {
          $scope.finding.valorRiesgo = "(:r) Tolerable".replace(":r", vRiesgo.toFixed(1));
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
        $scope.modalTitle = $translate.instant("confirmmodal.title_description");
        $scope.ok = function ok () {
          // Consumir el servicio
          const req = projectFtry.UpdateDescription(updateData);
          // Capturar la Promisse
          req.then((response) => {
            if (!response.error) {
              const updatedAt = $translate.instant("proj_alerts.updatedTitle");
              const updatedAc = $translate.instant("proj_alerts.updated_cont");
              $msg.success(updatedAc, updatedAt);
              $uibModalInstance.close();
              location.reload();
              // Tracking mixpanel
              mixPanelDashboard.trackFinding("UpdateFinding", userEmail, descData.id);
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
  };
  $scope.validateTreatment = function validateTreatment () {
    if ($scope.aux.razon === $scope.finding.razonTratamiento) {
      $msg.error($translate.instant("proj_alerts.differ_comment"));
      return false;
    }
    else if ($scope.finding.razonTratamiento === "") {
      $msg.error($translate.instant("proj_alerts.empty_comment"));
      return false;
    }
    else if ($scope.finding.razonTratamiento.length < 50 || $scope.finding.razonTratamiento.length > 80) {
      $msg.error($translate.instant("proj_alerts.short_comment"));
      return false;
    }
    $scope.finding.responsableTratamiento = userEmail;
    return true;
  };
  $scope.updateTreatment = function updateTreatment () {
    let flag = false;
    if ($scope.aux.tratamiento === $scope.finding.tratamiento && $scope.aux.razon === $scope.finding.razonTratamiento &&
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
          $scope.modalTitle = $translate.instant("search_findings.tab_description.update_treatmodal");
          $scope.ok = function ok () {
            // Consumir el servicio
            const req = projectFtry.UpdateTreatment(updateData);
            // Capturar la Promisse
            req.then((response) => {
              if (!response.error) {
                const org = Organization.toUpperCase();
                const projt = $stateParams.project.toUpperCase();
                mixPanelDashboard.trackFindingDetailed("FindingUpdateTreatment", userName, userEmail, org, projt, newData.id);
                $msg.success($translate.instant("proj_alerts.updated_treat"), $translate.instant("proj_alerts.congratulation"));
                $uibModalInstance.close();
                location.reload();
              }
              else if (response.error) {
                Rollbar.error("Error: An error occurred updating treatment");
                const errorAc1 = $translate.instant("proj_alerts.error_textsad");
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
        $scope.modalTitle = $translate.instant("search_findings.tab_description.remediated_finding");
        $scope.ok = function ok () {
          $scope.remediatedData.userMail = mailData.userMail;
          $scope.remediatedData.findingName = mailData.findingName;
          $scope.remediatedData.project = mailData.project;
          $scope.remediatedData.findingUrl = mailData.findingUrl;
          $scope.remediatedData.findingId = mailData.findingId;
          $scope.remediatedData.findingVulns = mailData.findingVulns;
          $scope.remediatedData.justification = $scope.remediatedData.justification.trim();
          if ($scope.remediatedData.justification.length < 100) {
            $msg.error($translate.instant("proj_alerts.short_remediated_comment"));
          }
          else {
            // Consumir el servicio
            const req = projectFtry.FindingSolved($scope.remediatedData);
            // Capturar la Promisse
            req.then((response) => {
              if (!response.error) {
                // Tracking mixpanel
                const org = Organization.toUpperCase();
                const projt = descData.project.toUpperCase();
                mixPanelDashboard.trackFindingDetailed("FindingRemediated", userName, userEmail, org, projt, descData.findingId);
                $scope.remediated = response.data.remediated;
                $msg.success($translate.instant("proj_alerts.remediated_success"), $translate.instant("proj_alerts.updatedTitle"));
                $uibModalInstance.close();
                location.reload();
                const data = {};
                data.id = parseInt(Math.round(new Date() / 1000).toString() + (Math.random() * 10000).toString(9), 10);
                data.content = $scope.remediatedData.justification;
                data.parent = 0;
                data.email = $scope.remediatedData.userMail;
                data.findingName = $scope.remediatedData.findingName;
                data.project = $scope.remediatedData.project;
                data.findingUrl = $scope.remediatedData.findingUrl;
                data.remediated = true;
                const comment = projectFtry.addComment($scope.remediatedData.findingId, data);
              }
              else if (response.error) {
                Rollbar.error("Error: An error occurred when remediating the finding");
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
      const req = projectFtry.RemediatedView($scope.finding.id);
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
          Rollbar.error("Error: An error occurred when remediating/verifying the finding");
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
        $scope.modalTitle = $translate.instant("search_findings.tab_description.verified_finding");
        $scope.ok = function ok () {
          // Consumir el servicio
          const req = projectFtry.FindingVerified(mailData);
          // Capturar la Promisse
          req.then((response) => {
            if (!response.error) {
              // Tracking mixpanel
              const org = Organization.toUpperCase();
              const projt = descData.project.toUpperCase();
              mixPanelDashboard.trackFindingDetailed("FindingVerified", userName, userEmail, org, projt, descData.findingId);
              const updatedAt = $translate.instant("proj_alerts.updatedTitle");
              const updatedAc = $translate.instant("proj_alerts.verified_success");
              $msg.success(updatedAc, updatedAt);
              $uibModalInstance.close();
              location.reload();
            }
            else if (response.error) {
              Rollbar.error("Error: An error occurred when verifying the finding");
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
    $("html, body").animate({"scrollTop": $scope.currentScrollPosition}, "fast");
  };
  $scope.urlDescription = function urlDescription () {
    location.replace(`${window.location.href.split($stateParams.id)[0] + $stateParams.id}/description`);
  };
  $scope.urlSeverity = function urlSeverity () {
    location.replace(`${window.location.href.split($stateParams.id)[0] + $stateParams.id}/severity`);
  };
  $scope.urlTracking = function urlTracking () {
    location.replace(`${window.location.href.split($stateParams.id)[0] + $stateParams.id}/tracking`);
  };
  $scope.urlEvidence = function urlEvidence () {
    location.replace(`${window.location.href.split($stateParams.id)[0] + $stateParams.id}/evidence`);
  };
  $scope.urlExploit = function urlExploit () {
    location.replace(`${window.location.href.split($stateParams.id)[0] + $stateParams.id}/exploit`);
  };
  $scope.urlRecords = function urlRecords () {
    location.replace(`${window.location.href.split($stateParams.id)[0] + $stateParams.id}/records`);
  };
  $scope.urlComments = function urlComments () {
    location.replace(`${window.location.href.split($stateParams.id)[0] + $stateParams.id}/comments`);
  };
  $scope.init = function init () {
    const project = $stateParams.project;
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
    if (typeof project !== "undefined" &&
            project !== "") {
      $scope.project = project;
    }
    // Inicializacion para consulta de hallazgos
    $scope.configColorPalette();
    $scope.finding = {};
    $scope.finding.id = $stateParams.id;
    $scope.loadFindingByID($stateParams.id);
    $scope.goUp();
    const org = Organization.toUpperCase();
    const projt = project.toUpperCase();
    $scope.alertHeader(org, projt);
    if (window.location.hash.indexOf("description") !== -1) {
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
      $("#commentItem").removeClass("active");
      $("#comment").removeClass("active");
      // Tracking mixpanel
      mixPanelDashboard.trackFindingDetailed("FindingDescription", userName, userEmail, org, projt, $scope.finding.id);
    }
    if (window.location.hash.indexOf("severity") !== -1) {
      $("#infoItem").removeClass("active");
      $("#info").removeClass("active");
      $("#cssv2Item").addClass("active");
      $("#cssv2").addClass("active");
      $("#trackingItem").removeClass("active");
      $("#tracking").removeClass("active");
      $("#evidenceItem").removeClass("active");
      $("#evidence").removeClass("active");
      $("#exploitItem").removeClass("active");
      $("#exploit").removeClass("active");
      $("#commentItem").removeClass("active");
      $("#comment").removeClass("active");
      // Tracking mixpanel
      mixPanelDashboard.trackFindingDetailed("FindingSeverity", userName, userEmail, org, projt, $scope.finding.id);
    }
    if (window.location.hash.indexOf("tracking") !== -1) {
      $("#infoItem").removeClass("active");
      $("#info").removeClass("active");
      $("#cssv2Item").removeClass("active");
      $("#cssv2").removeClass("active");
      $("#trackingItem").addClass("active");
      $("#tracking").addClass("active");
      $("#evidenceItem").removeClass("active");
      $("#evidence").removeClass("active");
      $("#exploitItem").removeClass("active");
      $("#exploit").removeClass("active");
      $("#commentItem").removeClass("active");
      $("#comment").removeClass("active");
      // Tracking mixpanel
      mixPanelDashboard.trackFindingDetailed("FindingTracking", userName, userEmail, org, projt, $scope.finding.id);
    }
    if (window.location.hash.indexOf("evidence") !== -1) {
      $("#infoItem").removeClass("active");
      $("#info").removeClass("active");
      $("#cssv2Item").removeClass("active");
      $("#cssv2").removeClass("active");
      $("#trackingItem").removeClass("active");
      $("#tracking").removeClass("active");
      $("#evidenceItem").addClass("active");
      $("#evidence").addClass("active");
      $("#exploitItem").removeClass("active");
      $("#exploit").removeClass("active");
      $("#commentItem").removeClass("active");
      $("#comment").removeClass("active");
      // Tracking mixpanel
      mixPanelDashboard.trackFindingDetailed("FindingEvidence", userName, userEmail, org, projt, $scope.finding.id);
    }
    if (window.location.hash.indexOf("exploit") !== -1) {
      $("#infoItem").removeClass("active");
      $("#info").removeClass("active");
      $("#cssv2Item").removeClass("active");
      $("#cssv2").removeClass("active");
      $("#trackingItem").removeClass("active");
      $("#tracking").removeClass("active");
      $("#evidenceItem").removeClass("active");
      $("#evidence").removeClass("active");
      $("#commentItem").removeClass("active");
      $("#comment").removeClass("active");
      $("#exploitItem").addClass("active");
      $("#exploit").addClass("active");
      // Tracking mixpanel
      mixPanelDashboard.trackFindingDetailed("FindingExploit", userName, userEmail, org, projt, $scope.finding.id);
    }
    if (window.location.hash.indexOf("records") !== -1) {
      $("#infoItem").removeClass("active");
      $("#info").removeClass("active");
      $("#cssv2Item").removeClass("active");
      $("#cssv2").removeClass("active");
      $("#trackingItem").removeClass("active");
      $("#tracking").removeClass("active");
      $("#evidenceItem").removeClass("active");
      $("#evidence").removeClass("active");
      $("#exploitItem").removeClass("active");
      $("#exploit").removeClass("active");
      $("#commentItem").removeClass("active");
      $("#comment").removeClass("active");
      $("#recordsItem").addClass("active");
      $("#records").addClass("active");
      $scope.findingRecordsTab();
      // Tracking mixpanel
      mixPanelDashboard.trackFindingDetailed("FindingRecords", userName, userEmail, org, projt, $scope.finding.id);
    }
    if (window.location.hash.indexOf("comments") !== -1) {
      $("#infoItem").removeClass("active");
      $("#info").removeClass("active");
      $("#cssv2Item").removeClass("active");
      $("#cssv2").removeClass("active");
      $("#trackingItem").removeClass("active");
      $("#tracking").removeClass("active");
      $("#evidenceItem").removeClass("active");
      $("#evidence").removeClass("active");
      $("#exploitItem").removeClass("active");
      $("#exploit").removeClass("active");
      $("#commentItem").addClass("active");
      $("#comment").addClass("active");
      $scope.findingCommentTab();
      // Tracking mixpanel
      mixPanelDashboard.trackFindingDetailed("FindingComments", userName, userEmail, org, projt, $scope.finding.id);
    }
  };
  $scope.init();
});
