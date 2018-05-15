/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global integrates, BASE, $xhr, response:true, Organization, $msg, $window,
$, Rollbar, eventsData, userEmail, userName, findingType, categories,
probabilities, actor, scenario, accessVector, accessComplexity, authentication,
confidenciality, integrity, availability, explotability, resolutionLevel,
realiabilityLevel, functionsFtry1, angular, mixPanelDashboard */
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "response"] }]*/
/**
 * @file functionsFtry2.js
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
angular.module("FluidIntegrates").factory(
  "functionsFtry2",
  ($injector, $stateParams, $translate, $window, projectFtry) => ({

    "activeTab" (tabName, errorName, org, projt, id) {
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
          angular.element(tabName).addClass("active");
          angular.element(tabNames[tabName]).addClass("active");
        }
        else {
          angular.element(Object.keys(tabNames)[inc]).removeClass("active");
          angular.element(tabNames[
            Object.keys(tabNames)[inc]]).removeClass("active");
        }
      }
      // Tracking mixpanel
      mixPanelDashboard.trackFindingDetailed(
        errorName,
        userName,
        userEmail,
        org,
        projt,
        id
      );
    },

    "evidenceEditable" ($scope) {
      if ($scope.onlyReadableTab3 === false) {
        $scope.onlyReadableTab3 = true;
      }
      else {
        $scope.onlyReadableTab3 = false;
      }
      // eslint-disable-next-line angular/document-service
      const inputs = document.querySelectorAll(".inputfile");
      angular.forEach.call(inputs, (input) => {
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
        angular.element("#evidenceText0").val(),
        angular.element("#evidenceText1").val(),
        angular.element("#evidenceText2").val(),
        angular.element("#evidenceText3").val(),
        angular.element("#evidenceText4").val(),
        angular.element("#evidenceText5").val(),
        angular.element("#evidenceText6").val()
      ];
      const refList = [];
      for (let cont = 0; cont < $scope.tabEvidences.length; cont++) {
        refList.push($scope.tabEvidences[cont].ref);
      }
      const evidence3 = 2;
      const evidence4 = 3;
      const evidence5 = 4;
      const evidence6 = 5;
      const evidence7 = 6;
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
      if (refList.indexOf(evidence3) === -1) {
        $scope.tabEvidences.push({
          "desc": "",
          "name": `${$translate.instant("search_findings." +
                                        "tab_evidence.evidence_name")} 1`,
          "ref": evidence3
        });
      }
      if (refList.indexOf(evidence4) === -1) {
        $scope.tabEvidences.push({
          "desc": "",
          "name": `${$translate.instant("search_findings." +
                                        "tab_evidence.evidence_name")} 2`,
          "ref": evidence4
        });
      }
      if (refList.indexOf(evidence5) === -1) {
        $scope.tabEvidences.push({
          "desc": "",
          "name": `${$translate.instant("search_findings." +
                                        "tab_evidence.evidence_name")} 3`,
          "ref": evidence5
        });
      }
      if (refList.indexOf(evidence6) === -1) {
        $scope.tabEvidences.push({
          "desc": "",
          "name": `${$translate.instant("search_findings." +
                                        "tab_evidence.evidence_name")} 4`,
          "ref": evidence6
        });
      }
      if (refList.indexOf(evidence7) === -1) {
        $scope.tabEvidences.push({
          "desc": "",
          "name": `${$translate.instant("search_findings." +
                                        "tab_evidence.evidence_name")} 5`,
          "ref": evidence7
        });
      }
      $scope.tabEvidences.sort((auxa, auxb) => auxa.ref - auxb.ref);
    },

    "exploitEditable" ($scope) {
      if ($scope.onlyReadableTab5 === false) {
        $scope.onlyReadableTab5 = true;
      }
      else {
        $scope.onlyReadableTab5 = false;
      }
      // eslint-disable-next-line angular/document-service
      const inputs = document.querySelectorAll(".inputfile");
      angular.forEach.call(inputs, (input) => {
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
    },

    "findingCalculateCSSv2" ($scope) {
      const calCSSv2 = projectFtry.calCCssv2($scope.severityInfo);
      const BaseScore = calCSSv2[0];
      const Temporal = calCSSv2[1];
      return [
        BaseScore.toFixed(1),
        Temporal.toFixed(1)
      ];
    },

    "findingInformationTab" ($scope) {
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
      $scope.finding.cardinalidad = parseInt($scope.finding.cardinalidad, 10);
      $scope.finding.criticidad = parseFloat($scope.finding.criticidad);
      const calCSSv2 = projectFtry.calCCssv2($scope.finding);
      const BaseScore = calCSSv2[0];
      const Temporal = calCSSv2[1];
      $scope.finding.cssv2base = BaseScore.toFixed(1);
      $scope.finding.criticidad = Temporal.toFixed(1);
      if ($scope.finding.nivel === "Detallado") {
        $scope.esDetallado = "show-detallado";
        $scope.esGeneral = "hide-detallado";
        const functionsFtry1 = $injector.get("functionsFtry1");
        const severityInfo = functionsFtry1.findingCalculateSeveridad();
        $scope.finding.valorRiesgo = severityInfo[1];
      }
      else {
        $scope.esDetallado = "hide-detallado";
        $scope.esGeneral = "show-detallado";
      }
    },

    "goDown" () {
      // eslint-disable-next-line angular/document-service
      $window.scrollTo(0, document.body.scrollHeight);
    },

    "recordsEditable" ($scope) {
      if ($scope.onlyReadableTab6 === false) {
        $scope.onlyReadableTab6 = true;
      }
      else {
        $scope.onlyReadableTab6 = false;
      }
      // eslint-disable-next-line angular/document-service
      const inputs = document.querySelectorAll(".inputfile");
      angular.forEach.call(inputs, (input) => {
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
    },

    "updateEvidencesFiles" (element, $scope) {
      let errorAc1 = " ";
      const evImage = angular.element(element).attr("target");
      const dataP = {};
      dataP.document = angular.element(`#evidence${evImage}`).val();
      if (dataP.document === "") {
        errorAc1 = $translate.instant("proj_alerts.error_textsad");
        $msg.error(errorAc1);
        return false;
      }
      const data = new FormData();
      const fileInput = angular.element(`#evidence${evImage}`)[0];
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
      const validateFileSize = function validateFileSize () {
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
        return true;
      };
      if (!validateFileSize()) {
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
