/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1,2,3,4,5,6,9,100.0,
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
    },

    "exploitEditable" ($scope) {
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
    },

    "findingCalculateCSSv2" ($scope) {
      const calCSSv2 = projectFtry.calCCssv2($scope.finding);
      const BaseScore = calCSSv2[0];
      const Temporal = calCSSv2[1];
      const CVSSGeneral = Temporal;
      return [
        BaseScore.toFixed(1),
        Temporal.toFixed(1)
      ];
    },

    "goDown" () {
      window.scrollTo(0, document.body.scrollHeight);
    },

    "recordsEditable" ($scope) {
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
