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
    projectFtry2
  ) {
    const initializeView = function initializeView () {
      // Users table configuration
      $scope.view.project = true;
      const translationStrings = [
        "search_findings.tab_users.edit",
        "search_findings.tab_users.add_button",
        "search_findings.tab_users.remove_user",

        "search_findings.tab_users.admin",
        "search_findings.tab_users.analyst",
        "search_findings.tab_users.customer",
        "search_findings.tab_users.customer_admin",
        "search_findings.tab_users.developer",

        "search_findings.tab_users.months_ago",
        "search_findings.tab_users.days_ago",
        "search_findings.tab_users.hours_ago",
        "search_findings.tab_users.minutes_ago",

        "search_findings.tab_users.success",
        "search_findings.tab_users.success_admin",
        "search_findings.tab_users.title",
        "search_findings.tab_users.edit_user_title",
        "search_findings.tab_users.textbox",
        "search_findings.tab_users.email",
        "search_findings.tab_users.user_organization",
        "search_findings.tab_users.user_responsibility",
        "search_findings.tab_users.responsibility_placeholder",
        "search_findings.tab_users.phone_number",
        "search_findings.tab_users.role",
        "search_findings.tab_users.success_delete",
        "search_findings.tab_users.title_success",
        "search_findings.tab_users.no_selection",

        "search_findings.users_table.usermail",
        "search_findings.users_table.userRole",
        "search_findings.users_table.userResponsibility",
        "search_findings.users_table.phoneNumber",
        "search_findings.users_table.userOrganization",
        "search_findings.users_table.firstlogin",
        "search_findings.users_table.lastlogin",

        "confirmmodal.cancel",
        "confirmmodal.proceed",

        "proj_alerts.access_denied",
        "proj_alerts.error_textsad"
      ];
      $scope.translations = {};
      angular.forEach(translationStrings, (value) => {
        $scope.translations[value] = $translate.instant(value);
      });
    };

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
      }
      functionsFtry3.configKeyboardView($scope);
      $scope.goUp();
      $scope.finding = {};
      projectFtry2.isCustomerAdmin(projectName, userEmail).
        then((response) => {
          if (angular.isUndefined(response)) {
            location.reload();
          }
          else if (response.data) {
            $scope.role = "customeradmin";
          }
          else {
            $scope.role = userRole;
          }
        });
      initializeView();
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
      }
      return true;
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
