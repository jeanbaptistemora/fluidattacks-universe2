/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow": ["$scope"] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, eventsData:true,
nonexploitLabel:true, totalHigLabel:true, exploitable:true, totalSegLabel:true,
openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg,
userName, userEmail, Rollbar, aux:true, json:true, closeLabel:true, j:true,
mixPanelDashboard, win:true, window, Organization, projectData:true, i:true,
eventsTranslations, keysToTranslate, labelEventState:true, angular, ldclient
*/
/**
 * @file projectEventsCtrl.js
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
 * @name projectEventsCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "projectEventsCtrl",
  function projectEventsCtrl (
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
    projectFtry
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
        const orgName = Organization.toUpperCase();
        const projName = projectName.toUpperCase();
        mixPanelDashboard.trackReports(
          "ProjectEvents",
          userName,
          userEmail,
          orgName,
          projName
        );
      }
      // Search function assignation to button and enter key configuration.
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
        if (eventsData.length > 0 &&
           eventsData[0].fluidProject.toLowerCase() ===
           $scope.project.toLowerCase()) {
          $scope.view.project = true;
          $scope.loadEventContent(eventsData, vlang, projectName);
        }
        else {
          const reqEventualities = projectFtry.eventualityByName(
            projectName,
            "Name"
          );
          reqEventualities.then((response) => {
            if (!response.error) {
              if (angular.isUndefined(response.data)) {
                location.reload();
              }
              $scope.view.project = true;
              eventsData = response.data;
              $scope.loadEventContent(eventsData, vlang, projectName);
            }
            else if (response.error) {
              if (response.message === "Access to project denied") {
                $msg.error($translate.instant("proj_alerts.access_denied"));
              }
              else {
                $msg.error($translate.instant("proj_alerts.eventExist"));
              }
            }
          });
        }
      }
      return true;
    };
    $scope.loadEventContent = function loadEventContent (data, vlang, project) {
      const organizationName = Organization.toUpperCase();
      const projectName = project.toUpperCase();
      functionsFtry1.alertHeader(organizationName, projectName);
      for (let cont = 0; cont < data.length; cont++) {
        for (let inc = 0; inc < eventsTranslations.length; inc++) {
          if (data[cont][eventsTranslations[inc]] in keysToTranslate) {
            data[cont][eventsTranslations[inc]] =
                  $translate.instant(keysToTranslate[
                    data[cont][eventsTranslations[inc]]
                  ]);
          }
        }
      }
      $scope.isManager = userRole !== "customer" &&
                         userRole !== "customeradmin";
      mixPanelDashboard.trackSearch("SearchEventuality", userEmail, project);
      // Eventuality table configuration
      angular.element("#tblEventualities").bootstrapTable("destroy");
      angular.element("#tblEventualities").bootstrapTable({
        "cookie": true,
        "cookieIdTable": "saveIEvent",
        data,
        "locale": vlang,
        "onClickRow" (row) {
          const enableEventView =
                              ldclient.variation("new-event-window-ind", false);
          if (enableEventView) {
            $state.go("EventsDescription", {
              "id": row.id,
              "project": row.fluidProject.toLowerCase()
            });
          }
          else {
            $uibModal.open({
              "animation": true,
              "backdrop": "static",
              "controller" ($scope, $uibModalInstance, evt) {
                $scope.evt = evt;
                $scope.evt.isManager = userRole !== "customer" &&
                                       userRole !== "customeradmin";
                $scope.evt.onlyReadableEvt1 = true;
                // Mixpanel tracking
                const nameOrg = Organization.toUpperCase();
                const nameProj = project.toUpperCase();
                mixPanelDashboard.trackReadEventuality(
                  userName,
                  userEmail,
                  nameOrg,
                  nameProj,
                  evt.id
                );
                if ($scope.evt.affectation === "" ||
                    angular.isUndefined($scope.evt.affectation)) {
                  $scope.evt.affectation = "0";
                }
                $scope.evt.affectation = parseInt($scope.evt.affectation, 10);
                $scope.eventEdit = function eventEdit () {
                  if ($scope.evt.onlyReadableEvt1 === false) {
                    $scope.evt.onlyReadableEvt1 = true;
                  }
                  else {
                    $scope.evt.onlyReadableEvt1 = false;
                  }
                };
                $scope.okModalEditar = function okModalEditar () {
                  const neg = "negativo";
                  try {
                    if (angular.isUndefined($scope.evt.affectation)) {
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
                  const reqEvents = eventualityFactory.updateEvnt($scope.evt);
                  reqEvents.then((response) => {
                    if (!response.error) {
                      const updatedAt = $translate.instant("proj_alerts." +
                                                           "updatedTitle");
                      const updatedAc = $translate.instant("proj_alerts." +
                                                           "eventUpdated");
                      $msg.success(updatedAc, updatedAt);
                      $uibModalInstance.close();
                      location.reload();
                    }
                    else if (response.error) {
                      if (response.message === "Campos vacios") {
                        Rollbar.error("Error: An error " +
                                       "occurred updating events");
                        $msg.error($translate.instant("proj_alerts." +
                                                      "emptyField"));
                      }
                      else {
                        Rollbar.error("Error: An error occurred " +
                                      "updating events");
                        $msg.error($translate.instant("proj_alerts." +
                                                      "errorUpdatingEvent"));
                      }
                    }
                  });
                  return true;
                };
                $scope.close = function close () {
                  $uibModalInstance.close();
                };
              },
              "keyboard": false,
              "resolve": {"evt": row},
              "templateUrl": `${BASE.url}assets/views/` +
                             "project/eventualityMdl.html"
            });
          }
        }
      });
      angular.element("#tblEventualities").bootstrapTable("refresh");
      angular.element("#search_section").show();
      angular.element("[data-toggle=\"tooltip\"]").tooltip();
      if (!$scope.isManager) {
        $scope.openEvents = projectFtry.alertEvents(eventsData);
        $scope.atAlert = $translate.instant("main_content.eventualities." +
                                            "descSingularAlert1");
        if ($scope.openEvents === 1) {
          $scope.descAlert1 = $translate.instant("main_content.eventualities." +
                                                  "descSingularAlert2");
          $scope.descAlert2 = $translate.instant("main_content.eventualities." +
                                                  "descSingularAlert3");
          angular.element("#events_alert").show();
        }
        else if ($scope.openEvents > 1) {
          $scope.descAlert1 = $translate.instant("main_content.eventualities." +
                                                  "descPluralAlert1");
          $scope.descAlert2 = $translate.instant("main_content.eventualities." +
                                                  "descPluralAlert2");
          angular.element("#events_alert").show();
        }
      }
    };
    $scope.openModalEventAvance = function openModalEventAvance () {
      $uibModal.open({
        "animation": true,
        "backdrop": "static",
        "controller" ($scope, $uibModalInstance) {
          $scope.rowsEvent =
                 angular.element("#tblEventualities").bootstrapTable("getData");
          $scope.close = function close () {
            $uibModalInstance.close();
            const TIMEOUT = 100;
            $timeout(() => {
              angular.element("#tblEventualities").bootstrapTable(
                "load",
                $scope.rowsEvent
              );
            }, TIMEOUT);
          };
        },
        "keyboard": false,
        "resolve": {"ok": true},
        "templateUrl": "avance.html",
        "windowClass": "modal avance-modal"
      });
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
