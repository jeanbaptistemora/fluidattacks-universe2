/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1, 3] }]*/
/* global integrates, BASE, $xhr, window.location:true, response:true,
Organization, mixPanelDashboard, mixPanelDashboard, mixPanelDashboard,$msg,
$, Rollbar, eventsData, userEmail, userName, secureRandom, angular*/
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "response"] }]*/
/**
 * @file tabsFtry.js
 * @author engineering@fluidattacks.com
 */
/**
 * Crea el factory de la funcionalidad de hallazgos
 * @name tabsFtry
 * @param {Object} $q Angular constructor
 * @param {Object} $translate Angular translator
 * @param {Object} projectFtry Factory with main functions
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory("tabsFtry", (
  $translate,
  projectFtry
) => ({
  "findingCommentTab" (commentInfo, $stateParams) {
    if (typeof commentInfo.finding.id !== "undefined") {
      const comments = projectFtry.getComments(commentInfo.finding.id);
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
          const TIMEOUT = 500;
          const divConst = 1000;
          const multiConst = 100;
          const radix = 9;
          angular.element("#comments-container").comments({
            "defaultNavigationSortKey": "oldest",
            "enableAttachments": false,
            "enableEditing": false,
            "enableHashtags": true,
            "enablePinging": false,
            "enableUpvoting": false,
            "getComments" (success) {
              setTimeout(() => {
                success(response.data);
              }, TIMEOUT);
            },
            "getUsers" (success) {
              setTimeout(() => {
                success(usersArray);
              }, TIMEOUT);
            },
            "postComment" (data, success) {
              data.id = parseInt(Math.round(new Date() / divConst).toString() +
                        (parseInt(secureRandom(3).join(""), 10) * multiConst).
                          toString(radix), 10);
              data.findingName = commentInfo.finding.hallazgo;
              data.project = commentInfo.finding.proyecto_fluid;
              data.findingUrl = window.location.href;
              data.remediated = false;
              const comment =
                         projectFtry.addComment(commentInfo.finding.id, data);
              comment.then((response) => {
                if (!response.error) {
                  // Tracking mixpanel
                  const org = Organization.toUpperCase();
                  const projt = $stateParams.project.toUpperCase();
                  mixPanelDashboard.trackFindingDetailed(
                    "FindingNewComment",
                    userName,
                    userEmail,
                    org,
                    projt,
                    commentInfo.finding.id
                  );
                  setTimeout(() => {
                    success(data);
                  }, TIMEOUT);
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
  },
  "findingEvidenceTab" (data) {
    const evidenceList = [];
    const updEvidenceList =
    function updEvidenceList (source, keyU, keyD, ref, type, array, scope) {
      const urlPre = `${window.location.href.split("dashboard#!/")[0] +
                      window.location.href.split("dashboard#!/")[1]}/`;
      const url = urlPre + source;
      let descText = "";
      if (type === "basic") {
        descText = $translate.instant(`search_findings.tab_evidence.${keyU}`);
      }
      else {
        descText = scope.finding[keyU];
      }
      array.push({
        "desc": descText,
        "name": $translate.instant(`search_findings.tab_evidence.${keyD}`),
        ref,
        url
      });
    };
    const setEvidenceList = function setEvidenceList (response, valFormstack) {
      for (let cont = 0; cont < response.data.length; cont++) {
        const valS3 = response.data[cont];
        if (typeof valS3.animacion !== "undefined" &&
                    valS3.es_animacion === true) {
          updEvidenceList(
            valS3.animacion, "animation_exploit",
            "animation_exploit", 0, "basic", evidenceList, data
          );
        }
        else if (typeof valFormstack.animacion !== "undefined") {
          updEvidenceList(
            valFormstack.animacion, "animation_exploit",
            "animation_exploit", 0, "basic", evidenceList, data
          );
        }
        if (typeof valS3.explotacion !== "undefined" &&
                   valS3.es_explotacion === true) {
          updEvidenceList(
            valS3.explotacion, "evidence_exploit",
            "evidence_exploit", 1, "basic", evidenceList, data
          );
        }
        else if (typeof valFormstack.explotacion !== "undefined") {
          updEvidenceList(
            valFormstack.explotacion, "evidence_exploit",
            "evidence_exploit", 1, "basic", evidenceList, data
          );
        }
        const evidenceAmong = 6;
        for (let inc = 1; inc < evidenceAmong; inc++) {
          if (typeof valFormstack[`desc_evidencia_${inc}`] !==
            "undefined" && typeof valS3[`ruta_evidencia_${inc}`] !==
            "undefined" && valS3[`es_ruta_evidencia_${inc}`] === true) {
            updEvidenceList(
              valS3[`ruta_evidencia_${inc}`], `desc_evidencia_${inc}`,
              "evidence_name", inc + 1, "special", evidenceList, data
            );
          }
          else if (typeof valFormstack[`desc_evidencia_${inc}`] !==
            "undefined" && typeof valFormstack[`ruta_evidencia_${inc}`] !==
            "undefined") {
            updEvidenceList(
              valFormstack[`ruta_evidencia_${inc}`],
              `desc_evidencia_${inc}`,
              "evidence_name", inc + 1, "special", evidenceList, data
            );
          }
        }
      }
    };
    const req = projectFtry.getEvidences(data.finding.id);
    req.then((response) => {
      if (!response.error) {
        const valFormstack = data.finding;
        if (response.data.length > 0) {
          setEvidenceList(response, valFormstack);
        }
        else {
          if (typeof data.finding.animacion !== "undefined") {
            updEvidenceList(
              valFormstack.animacion, "animation_exploit",
              "animation_exploit", 0, "basic", evidenceList, data
            );
          }
          if (typeof data.finding.explotacion !== "undefined") {
            updEvidenceList(
              valFormstack.explotacion, "evidence_exploit",
              "evidence_exploit", 1, "basic", evidenceList, data
            );
          }
          const evidenceAmong = 6;
          for (let inc = 1; inc < evidenceAmong; inc++) {
            if (typeof valFormstack[`desc_evidencia_${inc}`] !== "undefined" &&
                typeof valFormstack[`ruta_evidencia_${inc}`] !== "undefined") {
              updEvidenceList(
                valFormstack[`ruta_evidencia_${inc}`], `desc_evidencia_${inc}`,
                "evidence_name", inc + 1, "special", evidenceList, data
              );
            }
          }
        }
      }
      else if (response.error) {
        Rollbar.error("Error: An error occurred loading evidences");
      }
    });
    return evidenceList;
  },
  "findingExploitTab" (data, findingData) {
    data.hasExploit = false;
    findingData.hasExploit = data.hasExploit;
    let exploit = {};
    const req = projectFtry.getEvidences(data.finding.id);
    req.then((response) => {
      if (!response.error) {
        if (response.data.length > 0) {
          /* eslint func-style: ["error", "expression"]*/
          const respFunction = function respFunction (response) {
            if (!response.error) {
              let responses = response.replaceAll("<", "&lt;");
              responses = response.replaceAll(">", "&gt;");
              data.exploitURL = responses;
              findingData.exploitURL = data.exploitURL;
            }
            else if (response.error) {
              Rollbar.error("Error: An error occurred loading exploit from S3");
            }
          };
          for (let cont = 0; cont < response.data.length; cont++) {
            if (typeof response.data[cont].exploit !== "undefined" &&
                            response.data[cont].es_exploit === true &&
                              data.finding.cierres.length === 0) {
              exploit = projectFtry.getExploit(
                data.finding.id,
                response.data[cont].exploit
              );
              data.hasExploit = true;
              findingData.hasExploit = data.hasExploit;
              exploit.then((response) => {
                respFunction(response);
              });
            }
            else if (typeof data.finding.exploit !== "undefined" &&
                     data.finding.cierres.length === 0) {
              exploit = projectFtry.getExploit(
                data.finding.id,
                data.finding.exploit
              );
              data.hasExploit = true;
              findingData.hasExploit = data.hasExploit;
              exploit.then((response) => {
                respFunction(response);
              });
            }
            else {
              data.hasExploit = false;
              findingData.hasExploit = data.hasExploit;
            }
          }
        }
        else if (typeof data.finding.exploit !== "undefined" &&
                 data.finding.cierres.length === 0) {
          exploit = projectFtry.getExploit(
            data.finding.id,
            data.finding.exploit
          );
          data.hasExploit = true;
          findingData.hasExploit = data.hasExploit;
          exploit.then((response) => {
            if (!response.error) {
              let responses = response.replaceAll("<", "&lt;");
              responses = response.replaceAll(">", "&gt;");
              data.exploitURL = responses;
              findingData.exploitURL = data.exploitURL;
            }
            else if (response.error) {
              Rollbar.error("Error: An error occurred loading exploit");
            }
          });
        }
        else {
          data.hasExploit = false;
          findingData.hasExploit = data.hasExploit;
        }
      }
    });
    return [
      data.hasExploit,
      data.exploitURL,
      findingData.hasExploit,
      findingData.exploitURL
    ];
  },
  "findingRecordsTab" (data, findingData) {
    data.hasRecords = false;
    findingData.hasRecords = data.hasRecords;
    let vlang = "en-US";
    let record = {};
    const req = projectFtry.getEvidences(data.finding.id);
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
              angular.element("#recordsTable").bootstrapTable("destroy");
              angular.element("#recordsTable").bootstrapTable({
                "columns": dataCols,
                "cookie": true,
                "cookieIdTable": "recordsTableCookie",
                "data": response.data,
                "locale": vlang
              });
              angular.element("#recordsTable").bootstrapTable("refresh");
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
              record = projectFtry.getRecords(
                data.finding.id,
                response.data[cont].registros_archivo
              );
              data.hasRecords = true;
              findingData.hasRecords = data.hasRecords;
              record.then((response) => {
                respFunction(response);
              });
            }
            else if (typeof data.finding.registros_archivo !== "undefined") {
              record = projectFtry.getRecords(
                data.finding.id,
                data.finding.registros_archivo
              );
              data.hasRecords = true;
              findingData.hasRecords = data.hasRecords;
              record.then((response) => {
                respFunction(response);
              });
            }
            else if ((
              typeof data.finding.registros_archivo === "undefined" ||
              typeof response.data[cont].registros_archivo === "undefined") &&
              response.data[cont].es_registros_archivo === false) {
              data.hasRecords = false;
              findingData.hasRecords = data.hasRecords;
            }
          }
        }
        else if (typeof data.finding.registros_archivo !== "undefined") {
          record = projectFtry.getRecords(
            data.finding.id,
            data.finding.registros_archivo
          );
          data.hasRecords = true;
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
              angular.element("#recordsTable").bootstrapTable("destroy");
              angular.element("#recordsTable").bootstrapTable({
                "columns": dataCols,
                "cookie": true,
                "cookieIdTable": "recordsTableCookie",
                "data": response.data,
                "locale": vlang
              });
              angular.element("#recordsTable").bootstrapTable("refresh");
            }
            else if (response.error) {
              Rollbar.error("Error: An error occurred loading record");
              const errorAc1 = $translate.instant("proj_alerts.error_textsad");
              $msg.error(errorAc1);
            }
          });
        }
        else if (response.data.length <= 0 ||
                 typeof data.finding.registros_archivo === "undefined") {
          data.hasRecords = false;
          findingData.hasRecords = data.hasRecords;
        }
      }
    });
    return [
      data.hasRecords,
      findingData.hasRecords
    ];
  }
}));
