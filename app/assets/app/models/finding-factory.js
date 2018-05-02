/* eslint no-magic-numbers: ["error", { "ignore": [0,9,500,1000,10000] }]*/
/* global integrates, BASE, $xhr, window.location:true, response:true,
Organization, mixPanelDashboard, mixPanelDashboard, mixPanelDashboard,$msg,
$, Rollbar, eventsData, userEmail, userName */
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "response"] }]*/
/**
 * @file finding-factory.js
 * @author engineering@fluidattacks.com
 */
/**
 * Crea el factory de la funcionalidad de hallazgos
 * @name findingFtry
 * @param {Object} $q Angular constructor
 * @param {Object} $translate Angular translator
 * @param {Object} projectFtry Factory with main functions
 * @return {undefined}
 */
/** @export */
integrates.factory("findingFtry", ($q, $translate, projectFtry) => ({
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
          const saveComment = function saveComment (data) {
            // Convert pings to human readable format
            $(data.pings).each((index, id) => {
              const userInfo =
                        usersArray.filter((user) => userInfo.id === id)[0];
              data.content =
                        data.content.replace(`@${id}`, `@${userInfo.fullname}`);
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
              data.id = parseInt(Math.round(new Date() / 1000).toString() +
                        (Math.random() * 10000).toString(9), 10);
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
