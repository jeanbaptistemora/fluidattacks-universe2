/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow": ["$scope"] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, usersData:true,
nonexploitLabel:true, totalHigLabel:true, exploitable:true, totalSegLabel:true,
openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg,
userName, userEmail, Rollbar, aux:true, json:true, closeLabel:true, j:true,
mixPanelDashboard, win:true, window, Organization, projectData:true, i:true,
eventsTranslations, keysToTranslate, labelEventState:true, angular, parsley
*/
/**
 * @file projectUsersCtrl.js
 * @author engineering@fluidattacks.com
 */
/**
 * @function labelEventState
 * @param {string} value Status of an eventuality
 * @member integrates.registerCtrl
 * @return {string|boolean} Html code for specific label
 */
/* eslint-disable-next-line  func-name-matching */
labelEventState = function labelEventStateFunction (value) {
  if (value === "Tratada") {
    return "<label class='label label-success' style='background-color: " +
           "#31c0be'>Tratada</label>";
  }
  else if (value === "Solved") {
    return "<label class='label label-success' style='background-color: " +
           "#31c0be'>Solved</label>";
  }
  else if (value === "Pendiente") {
    return "<label class='label label-danger' style='background-color: " +
           "#f22;'>Pendiente</label>";
  }
  else if (value === "Unsolved") {
    return "<label class='label label-danger' style='background-color: " +
           "#f22;'>Unsolved</label>";
  }
  return false;
};

/**
 * Controller definition for eventuality view.
 * @name projectUsersCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "projectUsersCtrl",
  function projectUsersCtrl (
    $location,
    $scope,
    $state,
    $stateParams,
    $timeout,
    $translate,
    $uibModal,
    eventualityFactory,
    functionsFtry1,
    functionsFtry3,
    functionsFtry4,
    intlTelInputOptions,
    projectFtry,
    usersFtry
  ) {
    $scope.init = function init () {
      const projectName = $stateParams.project;
      const findingId = $stateParams.finding;
      $scope.userRole = userRole;
      functionsFtry4.verifyRoles($scope, projectName, userEmail, userRole);
      // Default flags value for view visualization
      $scope.view = {};
      $scope.view.project = false;
      $scope.view.finding = false;
      // Route parameters
      if (angular.isDefined(findingId)) {
        $scope.findingId = findingId;
      }
      if (angular.isDefined(projectName) &&
                projectName !== "") {
        $scope.project = projectName;
        $scope.search();
        $scope.loadUsersInfo(projectName, $scope.usersData);
      }
      functionsFtry3.configKeyboardView($scope);
      $scope.goUp();
      $scope.finding = {};
    };
    $scope.goUp = function goUp () {
      angular.element("html, body").animate({"scrollTop": 0}, "fast");
    };
    $scope.search = function search () {
      const projectName = $scope.project;
      if (angular.isUndefined(projectName) ||
                projectName === "") {
        const attentionAt = $translate.instant("proj_alerts.attentTitle");
        const attentionAc = $translate.instant("proj_alerts.attent_cont");
        $msg.warning(attentionAc, attentionAt);
        return false;
      }
      if ($stateParams.project !== $scope.project) {
        $state.go("ProjectIndicators", {"project": $scope.project});
      }
      else if ($stateParams.project === $scope.project) {
        $scope.view.project = false;
        $scope.view.finding = false;

        // Handling presentation button
        const searchAt = $translate.instant("proj_alerts.search_title");
        const searchAc = $translate.instant("proj_alerts.search_cont");
        $msg.info(searchAc, searchAt);
        const reqUsersLogin = projectFtry.usersByProject(projectName);
        reqUsersLogin.then((response) => {
          if (!response.error) {
            if (angular.isUndefined(response.data)) {
              location.reload();
            }
            else {
              $scope.view.project = true;
              const usersData = response.data.projectUsers;
              angular.forEach(usersData, (user) => {
                user.role = $translate.instant(`${"search_findings." +
                                              "tab_users."}${user.role}`);
                user.lastLogin = angular.fromJson(user.lastLogin);
                const DAYS_IN_MONTH = 30;
                if (user.lastLogin[0] >= DAYS_IN_MONTH) {
                  const ROUNDED_MONTH = Math.round(user.lastLogin[0] /
                                                 DAYS_IN_MONTH);
                  user.lastLogin = ROUNDED_MONTH +
                                    $translate.instant("search_findings." +
                                                  "tab_users.months_ago");
                }
                else if (user.lastLogin[0] > 0 &&
                         user.lastLogin[0] < DAYS_IN_MONTH) {
                  user.lastLogin = user.lastLogin[0] +
                                    $translate.instant("search_findings." +
                                                  "tab_users.days_ago");
                }
                else if (user.lastLogin[0] === -1) {
                  user.lastLogin = "-";
                  user.firstLogin = "-";
                }
                else {
                  const SECONDS_IN_HOUR = 3600;
                  const ROUNDED_HOUR = Math.round(user.lastLogin[1] /
                                                 SECONDS_IN_HOUR);
                  const SECONDS_IN_MINUTES = 60;
                  const ROUNDED_MINUTES = Math.round(user.lastLogin[1] /
                                                    SECONDS_IN_MINUTES);
                  if (ROUNDED_HOUR >= 1 &&
                      ROUNDED_MINUTES >= SECONDS_IN_MINUTES) {
                    user.lastLogin = ROUNDED_HOUR +
                                  $translate.instant("search_findings." +
                                                "tab_users.hours_ago");
                  }
                  else {
                    user.lastLogin = ROUNDED_MINUTES +
                                    $translate.instant("search_findings." +
                                                  "tab_users.minutes_ago");
                  }
                }
              });
              $scope.loadUsersInfo(projectName, usersData);
            }
          }
          else if (response.error) {
            if (response.message === "Access denied") {
              $msg.error($translate.instant("proj_alerts.access_denied"));
            }
            else {
              Rollbar.warning("Warning: Users not found");
              $msg.error($translate.instant("proj_alerts.error_textsad"));
            }
          }
        });
      }
      return true;
    };

    $scope.loadUsersInfo = function loadUsersInfo (project, data) {
      // Users table configuration
      $scope.tblUsersHeaders = [
        {
          "dataField": "email",
          "header": $translate.instant("search_findings.users_table.usermail"),
          "width": "27%"
        },
        {
          "dataField": "role",
          "header":
          $translate.instant("search_findings.users_table.userRole"),
          "width": "8%"
        },
        {
          "dataField": "responsability",
          "header":
          $translate.instant("search_findings.users_table.userResponsibility"),
          "width": "12%"
        },
        {
          "dataField": "phoneNumber",
          "header":
          $translate.instant("search_findings.users_table.phoneNumber"),
          "width": "10%"
        },
        {
          "dataField": "organization",
          "header":
          $translate.instant("search_findings.users_table.userOrganization"),
          "width": "10%"
        },
        {
          "dataField": "firstLogin",
          "header":
          $translate.instant("search_findings.users_table.firstlogin"),
          "width": "12%"
        },
        {
          "dataField": "lastLogin",
          "header":
          $translate.instant("search_findings.users_table.lastlogin"),
          "width": "12%"
        }
      ];
      $scope.usersDataset = data;
    };

    $scope.addUser = function addUser () {
      usersFtry.addUser($scope);
    };

    $scope.editUser = function editUser () {
      usersFtry.editUser($scope);
    };

    $scope.removeUserAccess = function removeUserAccess () {
      usersFtry.removeUserAccess($scope);
    };

    $scope.urlIndicators = function urlIndicators () {
      $state.go("ProjectIndicators", {"project": $scope.project});
    };
    $scope.urlFindings = function urlFindings () {
      $state.go("ProjectFindings", {"project": $scope.project});
    };
    $scope.urlEvents = function urlEvents () {
      $state.go("ProjectEvents", {"project": $scope.project});
    };
    $scope.urlUsers = function urlUsers () {
      $state.go("ProjectUsers", {"project": $scope.project});
    };
    $scope.urlDrafts = function urlDrafts () {
      $state.go("ProjectDrafts", {"project": $scope.project});
    };
    $scope.urlResources = function urlResources () {
      $state.go("ProjectResources", {"project": $scope.project});
    };
    $scope.init();
  }
);
