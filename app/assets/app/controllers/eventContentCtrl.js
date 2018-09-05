/* eslint no-magic-numbers:
["error", { "ignore": [-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "$state","response"] }]*/
/* global
angular, $msg, Rollbar, userRole, eventsTranslations, keysToTranslate
*/
/**
 * @file eventContentCtrl.js
 * @author engineering@fluidattacks.com
 */
/**
 * Controller definition for finding content view.
 * @name eventContentCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $translate
 * @param {Object} ngNotify
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller("eventContentCtrl", function
eventContentCtrl (
  $scope,
  $state,
  $stateParams,
  $timeout,
  $translate,
  $uibModal,
  $window,
  eventualityFactory,
  functionsFtry1,
  functionsFtry2,
  functionsFtry3,
  functionsFtry4,
  ngNotify,
  projectFtry,
  projectFtry2
) {
  $scope.goUp = function goUp () {
    angular.element("html, body").animate({"scrollTop": 0}, "fast");
  };

  $scope.hasUrl = function hasUrl (element) {
    if (angular.isDefined(element)) {
      if (element.indexOf("https://") !== -1 ||
          element.indexOf("http://") !== -1) {
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
  $scope.loadEvent = function loadEvent (project, id) {
    const reqEventualities = projectFtry.eventByName(
      project,
      id
    );
    reqEventualities.then((response) => {
      if (!response.error) {
        if (angular.isUndefined(response.data)) {
          location.reload();
        }
        const eventData = response.data;
        for (let inc = 0; inc < eventsTranslations.length; inc++) {
          if (eventData[eventsTranslations[inc]] in keysToTranslate) {
            eventData[eventsTranslations[inc]] =
                    $translate.instant(keysToTranslate[
                      eventData[eventsTranslations[inc]]
                    ]);
          }
        }
        $scope.eventData = eventData;
      }
      else if (response.message === "Access to project denied") {
        $msg.error($translate.instant("proj_alerts.access_denied"));
      }
      else {
        $msg.error($translate.instant("proj_alerts.eventExist"));
      }
    });
  };

  $scope.eventEdit = function eventEdit () {
    if ($scope.isEditable === false) {
      $scope.isEditable = true;
    }
    else {
      $scope.isEditable = false;
    }
  };
  $scope.eventUpdate = function eventUpdate () {
    const neg = "negativo";
    try {
      if (angular.isUndefined($scope.eventData.affectation)) {
        throw neg;
      }
    }
    catch (err) {
      Rollbar.error("Error: Affectation can not " +
                    "be a negative number");
      $msg.error($translate.instant("proj_alerts." +
                                    "eventPositiveint"));
      return false;
    }
    const updateRequest = eventualityFactory.updateEvnt($scope.eventData);
    updateRequest.then((response) => {
      if (!response.error) {
        const alertTitle = $translate.instant("proj_alerts." +
                                             "updatedTitle");
        const alertContent = $translate.instant("proj_alerts." +
                                             "eventUpdated");
        $msg.success(alertContent, alertTitle);
        location.reload();
      }
      else if (response.error) {
        if (response.message === "Campos vacios") {
          Rollbar.error("Error: An error occurred updating events");
          $msg.error($translate.instant("proj_alerts.emptyField"));
        }
        else {
          Rollbar.error("Error: An error occurred updating events");
          $msg.error($translate.instant("proj_alerts." +
                                        "errorUpdatingEvent"));
        }
      }
    });
    return true;
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
  $scope.goBack = function goBack () {
    $state.go("ProjectEvents", {"project": $stateParams.project.toLowerCase()});
    angular.element("html, body").animate(
      {"scrollTop": $scope.currentScrollPosition},
      "fast"
    );
  };

  $scope.init = function init () {
    const projectName = $stateParams.project;
    const eventId = $stateParams.id;
    $scope.isEditable = false;
    $scope.userRole = userRole;
    // Flags for editable fields activation

    const hasAccess = projectFtry2.accessToProject(projectName);
    hasAccess.then((response) => {
      // Initialization of search findings function
      $scope.configColorPalette();
      $scope.loadEvent(projectName, eventId);
      $scope.goUp();
      if (!response.error) {
        $scope.hasAccess = response.data;
        $scope.isManager = userRole !== "customer" &&
                           userRole !== "customeradmin";
      }
      else if (response.error) {
        $scope.hasAccess = false;
        $scope.isManager = false;
        $msg.error($translate.instant("proj_alerts.access_denied"));
      }
    });
    // Default flags value for view visualization
    $scope.isAdmin = userRole !== "customer" &&
            userRole !== "customeradmin" && userRole !== "analyst";

    // Route parameters
    if (angular.isDefined(eventId)) {
      $scope.findingId = eventId;
    }
    if (angular.isDefined(projectName) &&
            projectName !== "") {
      $scope.project = projectName;
    }
  };
  $scope.init();
});
