/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow": ["$scope"] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, usersData:true,
nonexploitLabel:true, totalHigLabel:true, exploitable:true, totalSegLabel:true,
openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg,
userName, userEmail, Rollbar, aux:true, json:true, closeLabel:true, j:true,
mixPanelDashboard, win:true, window, Organization, projectData:true, i:true,
eventsTranslations, keysToTranslate, labelEventState:true, angular
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
labelEventState = function labelEventState (value) {
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
    projectFtry
  ) {
    $scope.init = function init () {
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
      const projectName = $stateParams.project;
      const findingId = $stateParams.finding;
      $scope.userRole = userRole;

      $scope.isManager = userRole !== "customer";
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
        $scope.loadUsersInfo(projectName, vlang, $scope.usersData);
      }
      functionsFtry3.configKeyboardView($scope);
      $scope.goUp();
      $scope.finding = {};
    };
    $scope.goUp = function goUp () {
      angular.element("html, body").animate({"scrollTop": 0}, "fast");
    };
    $scope.search = function search () {
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
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
            $scope.view.project = true;
            const usersData = response.data;
            $scope.loadUsersInfo(projectName, vlang, usersData);
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
      return true;
    };

    $scope.loadUsersInfo = function loadUsersInfo (project, vlang, data) {
      // Eventuality table configuration
      angular.element("#tblUsers").bootstrapTable("destroy");
      angular.element("#tblUsers").bootstrapTable({
        data,
        "locale": vlang
      });
      angular.element("#tblUsers").bootstrapTable("refresh");
      angular.element("#search_section").show();
      angular.element("[data-toggle=\"tooltip\"]").tooltip();
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
    $scope.init();
  }
);
