/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* eslint no-shadow: ["error", { "allow": ["$scope"] }]*/
/* global
BASE, downLink:true, Morris, estado:true, exploitLabel:true, i:true, j:true,
nonexploitLabel:true, totalHigLabel:true, exploitable:true, totalSegLabel:true,
openLabel:true, partialLabel:true, integrates, userRole, document, $, $msg,
userName, userEmail, Rollbar, aux:true, json:true, closeLabel:true, angular,
mixPanelDashboard, win:true, Organization, projectData:true, eventsData:true
*/
/* eslint-env node*/
/**
 * @file projectResourcesCtrl.js
 * @author engineering@fluidattacks.com
 */
/* Table Formatter */

/**
 * Controller definition for indicators tab view.
 * @name projectResourcesCtrl
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").controller(
  "projectResourcesCtrl",
  function projectResourcesCtrl (
    $location,
    $scope,
    $state,
    $stateParams,
    $timeout,
    $translate,
    $uibModal,
    functionsFtry1,
    functionsFtry3,
    functionsFtry4,
    projectFtry2
  ) {
    $scope.init = function init () {
      const projectName = $stateParams.project;
      const findingId = $stateParams.finding;
      $scope.userRole = userRole;
      functionsFtry4.verifyRoles($scope, projectName, userEmail, userRole);
      $scope.view = {};
      $scope.view.project = false;
      $scope.view.finding = false;
      // Route parameters.
      if (angular.isDefined(findingId)) {
        $scope.findingId = findingId;
      }
      if (angular.isDefined(projectName) &&
                projectName !== "") {
        $scope.project = projectName;
        $scope.search();
        const org = Organization.toUpperCase();
        const projt = projectName.toUpperCase();
        angular.element(".equalWidgetHeight").matchHeight();
        mixPanelDashboard.trackReports(
          "ProjectResources",
          userName,
          userEmail,
          org,
          projt
        );
      }
      // Search function assignation to button and enter key configuration.
      functionsFtry3.configKeyboardView($scope);
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
        const reqRepositories = projectFtry2.repositoriesByProject(projectName);
        reqRepositories.then((response) => {
          if (!response.error) {
            if (angular.isUndefined(response.data)) {
              location.reload();
            }
            $scope.view.project = true;
            const projectRepoInfo = response.data.repositories;
            $scope.loadRepoInfo(projectName, vlang, projectRepoInfo);
          }
          else if (response.error) {
            Rollbar.warning("Warning: Users not found");
            $msg.error($translate.instant("proj_alerts.error_textsad"));
          }
        });
      }
      return true;
    };

    $scope.loadRepoInfo = function loadRepoInfo (project, vlang, data) {
      // Eventuality table configuration

      angular.element("#tblRepositories").bootstrapTable("destroy");
      angular.element("#tblRepositories").bootstrapTable({
        "cookie": true,
        "cookieIdTable": "saveIdRepositories",
        data,
        "locale": vlang
      });
      angular.element("#tblRepositories").bootstrapTable("refresh");
      angular.element("#tblRepositories").bootstrapTable(
        "hideColumn",
        "selection"
      );
      if ($scope.isProjectManager || $scope.isAdmin) {
        angular.element("#tblRepositories").bootstrapTable(
          "showColumn",
          "selection"
        );
      }
      angular.element("#search_section").show();
      angular.element("[data-toggle=\"tooltip\"]").tooltip();
    };

    $scope.addRepository = function addRepository () {
      // Obtener datos
      const descData = {"project": $stateParams.project.toLowerCase()};
      $uibModal.open({
        "animation": true,
        "backdrop": "static",
        "controller" ($scope, $uibModalInstance, data) {
          $scope.repoInfo = {};
          $scope.modalTitle = $translate.instant("search_findings." +
                                          "tab_resources.title");
          $scope.repoInfo.repositories = [{"id": 1}];
          $scope.isFirst = true;
          $scope.addNewRepository = function addNewRepository () {
            const newItemNo = $scope.repoInfo.repositories.length + 1;
            $scope.isFirst = false;
            $scope.repoInfo.repositories.push({"id": newItemNo});
          };
          $scope.removeRepository = function removeRepository (id) {
            const index = parseInt(id, 10);
            if ($scope.repoInfo.repositories.length > 1) {
              $scope.repoInfo.repositories.splice(index - 1, 1);
            }
            else {
              $scope.isFirst = true;
            }
          };
          $scope.ok = function ok () {
            $scope.repoInfo.totalRepo = $scope.repoInfo.repositories.length;
            const inputValidations = angular.element(".repositoryInput");
            let repoValidation = true;
            let elem = 0;
            while (repoValidation && inputValidations.length > elem) {
              if (angular.element(`#${inputValidations[elem].id}`).parsley().
                validate() === true) {
                repoValidation = true;
              }
              else {
                repoValidation = false;
              }
              elem += 1;
            }
            if (repoValidation) {
              // Make the request
              const repo = projectFtry2.addRepositories(
                $scope.repoInfo,
                data.project
              );
              // Capture the promise
              repo.then((response) => {
                if (!response.error) {
                  // Mixpanel tracking
                  const projt = descData.project.toUpperCase();
                  mixPanelDashboard.trackSearch(
                    "addRepository",
                    userEmail,
                    projt
                  );
                  const message = $translate.instant("search_findings" +
                                                ".tab_resources.success");
                  const messageTitle = $translate.instant("search_findings" +
                                                ".tab_users.title_success");
                  $msg.success(message, messageTitle);
                  $uibModalInstance.close();
                  location.reload();
                }
                else if (response.error) {
                  Rollbar.error("Error: An error occurred when " +
                              "adding a new repository");
                  $msg.error($translate.instant("proj_alerts.error_textsad"));
                }
              });
            }
          };
          $scope.close = function close () {
            $uibModalInstance.close();
          };
        },
        "keyboard": false,
        "resolve": {"data": descData},
        "size": "lg",
        "templateUrl": `${BASE.url}assets/views/project/addRepositoryMdl.html`
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
