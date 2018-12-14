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
      }
    };
  }
);
