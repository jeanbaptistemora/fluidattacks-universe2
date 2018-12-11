/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1, 3] }]*/
/* global integrates, BASE, $xhr, $window, response:true,
Organization, $timeout, mixPanelDashboard, $msg, $, Rollbar, eventsData,
userEmail, userName, secureRandom, angular*/
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "response"] }]*/
/**
 * @file tabsFtry.js
 * @author engineering@fluidattacks.com
 */
/**
 * Factory definition for the tab initialization in finding view.
 * @name tabsFtry
 * @param {Object} $q Angular constructor
 * @param {Object} $translate Angular translator
 * @param {Object} projectFtry Factory with main functions
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "tabsFtry",
  function tabsFtryFunction (
    $timeout,
    $translate,
    $window,
    projectFtry
  ) {
    return {
      "findingCommentTab" (commentInfo, $stateParams, commentType) {
        if (angular.isDefined(commentInfo.finding.id)) {
          const comments =
                 projectFtry.getComments(
                   commentInfo.finding.id,
                   commentType
                 );
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
              angular.element(`#${commentType}s-container`).comments({
                "defaultNavigationSortKey": "oldest",
                "enableAttachments": false,
                "enableEditing": false,
                "enableHashtags": true,
                "enablePinging": false,
                "enableUpvoting": false,
                "getComments" (success) {
                  $timeout(() => {
                    success(response.data);
                  }, TIMEOUT);
                },
                "getUsers" (success) {
                  $timeout(() => {
                    success(usersArray);
                  }, TIMEOUT);
                },
                "postComment" (data, success) {
                  data.id = parseInt(Math.round(new Date() /
                           divConst).toString() +
                           (parseInt(secureRandom(3).join(""), 10) *
                            multiConst).toString(radix), 10);
                  data.findingName = commentInfo.finding.finding;
                  data.project = commentInfo.finding.projectName;
                  data.findingUrl = $window.location.href;
                  data.remediated = false;
                  data.commentType = commentType;
                  const comment =
                         projectFtry.addComment(commentInfo.finding.id, data);
                  comment.then((response) => {
                    if (!response.error) {
                      // Mixpanel tracking
                      const org = Organization.toUpperCase();
                      const projt = $stateParams.project.toUpperCase();
                      const eventName = "FindingNew" +
                        `${commentType[0].toUpperCase()}` +
                        `${commentType.slice(1)}`;
                      mixPanelDashboard.trackFindingDetailed(
                        eventName,
                        userName,
                        userEmail,
                        org,
                        projt,
                        commentInfo.finding.id
                      );
                      $timeout(() => {
                        success(data);
                      }, TIMEOUT);
                    }
                    else if (response.error) {
                      Rollbar.error("Error: An error occurred adding" +
                        `${commentType}`);
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
          const urlPre = `${$window.location.href.split("dashboard#!/")[0] +
                      $window.location.href.split("dashboard#!/")[1]}/`;
          const url = urlPre + source;
          let descText = "";
          if (type === "basic") {
            descText = $translate.instant("search_findings." +
                                          `tab_evidence.${keyU}`);
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
        const formatEvidences = function formatEvidences (response) {
          const evidencesS3 = {};
          const TOTAL_EVIDENCES = 5;
          for (let file = 0; file < response.data.length; file++) {
            if (response.data[file].name === "animation") {
              evidencesS3.animation = response.data[file].file_url;
            }
            else if (response.data[file].name === "exploitation") {
              evidencesS3.exploitation = response.data[file].file_url;
            }
            else {
              for (let ev = 1; ev <= TOTAL_EVIDENCES; ev++) {
                if (response.data[file].name === `evidence_route_${ev}`) {
                  evidencesS3[`evidence_route_${ev}`] =
                    response.data[file].file_url;
                }
              }
            }
          }
          return evidencesS3;
        };
        const setEvidenceList =
        function setEvidenceList (valS3, valFormstack) {
          if (angular.isDefined(valS3.animation)) {
            updEvidenceList(
              valS3.animation, "animation_exploit",
              "animation_exploit", 0, "basic", evidenceList, data
            );
          }
          else if (angular.isDefined(valFormstack.animation)) {
            updEvidenceList(
              valFormstack.animation, "animation_exploit",
              "animation_exploit", 0, "basic", evidenceList, data
            );
          }
          if (angular.isDefined(valS3.exploitation)) {
            updEvidenceList(
              valS3.exploitation, "evidence_exploit",
              "evidence_exploit", 1, "basic", evidenceList, data
            );
          }
          else if (angular.isDefined(valFormstack.exploitation)) {
            updEvidenceList(
              valFormstack.exploitation, "evidence_exploit",
              "evidence_exploit", 1, "basic", evidenceList, data
            );
          }
          const evidenceAmong = 6;
          for (let inc = 1; inc < evidenceAmong; inc++) {
            if (angular.isDefined(valFormstack["evidence_" +
                `description_${inc}`]) &&
                angular.isDefined(valS3[`evidence_route_${inc}`])) {
              updEvidenceList(
                valS3[`evidence_route_${inc}`], `evidence_description_${inc}`,
                "evidence_name", inc + 1, "special", evidenceList, data
              );
            }
            else if (angular.isDefined(valFormstack["evidence_" +
                  `description_${inc}`]) &&
                   angular.isDefined(valFormstack[`evidence_route_${inc}`])) {
              updEvidenceList(
                valFormstack[`evidence_route_${inc}`],
                `evidence_description_${inc}`,
                "evidence_name", inc + 1, "special", evidenceList, data
              );
            }
          }
        };
        const req = projectFtry.getEvidences(data.finding.id);
        req.then((response) => {
          if (!response.error) {
            const valFormstack = data.finding;
            if (response.data.length > 0) {
              const evidencesS3 = formatEvidences(response);
              setEvidenceList(evidencesS3, valFormstack);
            }
            else {
              if (angular.isDefined(data.finding.animation)) {
                updEvidenceList(
                  valFormstack.animation, "animation_exploit",
                  "animation_exploit", 0, "basic", evidenceList, data
                );
              }
              if (angular.isDefined(data.finding.exploitation)) {
                updEvidenceList(
                  valFormstack.exploitation, "evidence_exploit",
                  "evidence_exploit", 1, "basic", evidenceList, data
                );
              }
              const evidenceAmong = 6;
              for (let inc = 1; inc < evidenceAmong; inc++) {
                if (angular.isDefined(valFormstack["evidence_" +
                  `description_${inc}`]) &&
                  angular.isDefined(valFormstack[`evidence_route_${inc}`])) {
                  updEvidenceList(
                    valFormstack[`evidence_route_${inc}`],
                    `evidence_description_${inc}`, "evidence_name", inc + 1,
                    "special", evidenceList, data
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
        const req = projectFtry.getEvidences(data.finding.id);
        req.then((response) => {
          if (!response.error) {
            if (response.data.length > 0) {
              const exploitS3 = {};
              for (let cont = 0; cont < response.data.length; cont++) {
                if (response.data[cont].name === "exploit") {
                  exploitS3.exploit = response.data[cont].file_url;
                }
              }
              if (angular.isDefined(exploitS3.exploit) &&
                      data.finding.cierres.length === 0) {
                data.hasExploit = true;
                findingData.hasExploit = data.hasExploit;
              }
              else if (angular.isDefined(data.finding.exploit) &&
                   data.finding.cierres.length === 0) {
                data.hasExploit = true;
                findingData.hasExploit = data.hasExploit;
              }
              else {
                data.hasExploit = false;
                findingData.hasExploit = data.hasExploit;
              }
            }
            else if (angular.isDefined(data.finding.exploit) &&
                 data.finding.cierres.length === 0) {
              data.hasExploit = true;
              findingData.hasExploit = data.hasExploit;
            }
            else {
              data.hasExploit = false;
              findingData.hasExploit = data.hasExploit;
            }
          }
        });
        return [
          data.hasExploit,
          data.exploitSrc,
          findingData.hasExploit,
          findingData.exploitSrc
        ];
      }
    };
  }
);
