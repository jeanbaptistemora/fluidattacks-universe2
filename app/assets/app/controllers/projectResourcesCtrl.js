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
        $scope.loadResourcesInfo(projectName);
      }
      return true;
    };

    $scope.loadResourcesInfo = function loadResourcesInfo (projectName) {
      $scope.tblReposHeaders = [
        {
          "dataField": "urlRepo",
          "header":
            $translate.instant("search_findings.repositories_table.repository"),
          "width": "70%"
        },
        {
          "dataField": "branch",
          "header":
            $translate.instant("search_findings.repositories_table.branch"),
          "width": "30%"
        }
      ];
      $scope.tblEnvsHeaders = [
        {
          "dataField": "urlEnv",
          "header":
            $translate.instant("search_findings.environment_table.environment")
        }
      ];
      const reqResources = projectFtry2.resourcesByProject(projectName);
      $scope.reposDataset = [];
      $scope.envsDataset = [];

      reqResources.then((response) => {
        if (response.error) {
          if (response.message === "Access denied") {
            $msg.error($translate.instant("proj_alerts.access_denied"));
          }
          else {
            Rollbar.warning("Warning: Resources not found");
            $msg.error($translate.instant("proj_alerts.error_textsad"));
          }
        }
        else if (angular.isUndefined(response.data)) {
          location.reload();
        }
        else {
          $scope.view.project = true;
          const respData = response.data.resources;
          if (respData.access) {
            $scope.reposDataset = angular.fromJson(respData.repositories);
            $scope.envsDataset = angular.fromJson(respData.environments);
          }
          else {
            $msg.error($translate.instant("proj_alerts.access_denied"));
          }
        }
      });
    };

    $scope.removeRepository = function removeRepository () {
      const selectedRow =
        angular.element("#tblRepositories tr input:checked").closest("tr");
      if (selectedRow.length > 0) {
        const REPOSITORY_INDEX = 1;
        const BRANCH_INDEX = 2;
        const repository = selectedRow.children()[REPOSITORY_INDEX].textContent;
        const branch = selectedRow.children()[BRANCH_INDEX].textContent;
        const repositories = {};
        repositories.urlRepo = repository;
        repositories.branch = branch;
        const project = $stateParams.project.toLowerCase();
        const repo = projectFtry2.removeRepositories(
          angular.toJson(angular.toJson(repositories)),
          project
        );
        // Capture the promise
        repo.then((response) => {
          if (response.error) {
            Rollbar.error("Error: An error occurred when removing repository");
            $msg.error($translate.instant("proj_alerts.error_textsad"));
          }
          else {
            // Mixpanel tracking
            const projt = project.toUpperCase();
            mixPanelDashboard.trackSearch(
              "removeRepository",
              userEmail,
              projt
            );
            const respData = response.data.removeRepositories;
            if (respData.success) {
              const message = $translate.instant("search_findings" +
                                            ".tab_resources.success_remove");
              const messageTitle = $translate.instant("search_findings" +
                                            ".tab_users.title_success");
              $msg.success(message, messageTitle);
              const repos = respData.resources.repositories;
              $scope.reposDataset = angular.fromJson(repos);
            }
            else if (respData.access) {
              Rollbar.error("Error: An error occurred when removing a " +
              "repository");
              $msg.error($translate.instant("proj_alerts.error_textsad"));
            }
            else {
              $msg.error($translate.instant("proj_alerts.access_denied"));
            }
          }
        });
      }
      else {
        $msg.error($translate.instant("search_findings.tab_resources" +
                                      ".no_selection"));
      }
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
                                          "tab_resources.title_repo");
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
                angular.toJson(angular.toJson($scope.repoInfo)),
                data.project
              );
              // Capture the promise
              repo.then((response) => {
                if (response.error) {
                  Rollbar.error("Error: An error occurred when " +
                              "adding a new repository");
                  $msg.error($translate.instant("proj_alerts.error_textsad"));
                }
                else {
                  // Mixpanel tracking
                  const projt = descData.project.toUpperCase();
                  mixPanelDashboard.trackSearch(
                    "addRepository",
                    userEmail,
                    projt
                  );
                  const respData = response.data.addRepositories;
                  if (respData.success) {
                    const message = $translate.instant("search_findings" +
                                                  ".tab_resources.success");
                    const messageTitle = $translate.instant("search_findings" +
                                                  ".tab_users.title_success");
                    $msg.success(message, messageTitle);
                    const repos = respData.resources.repositories;
                    $scope.$parent.reposDataset = angular.fromJson(repos);
                  }
                  else if (respData.access) {
                    Rollbar.error("Error: An error occurred when adding a " +
                    "repository");
                    $msg.error($translate.instant("proj_alerts.error_textsad"));
                  }
                  else {
                    $msg.error($translate.instant("proj_alerts.access_denied"));
                  }
                  $uibModalInstance.close();
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
        "scope": $scope,
        "size": "lg",
        "templateUrl": `${BASE.url}assets/views/project/addRepositoryMdl.html`
      });
    };

    $scope.addEnvironment = function addEnvironment () {
      const descData = {"project": $stateParams.project.toLowerCase()};
      $uibModal.open({
        "animation": true,
        "backdrop": "static",
        "controller" ($scope, $uibModalInstance, data) {
          $scope.envInfo = {};
          $scope.modalTitle = $translate.instant("search_findings." +
                                          "tab_resources.title_env");
          $scope.envInfo.environments = [{"id": 1}];
          $scope.isFirst = true;
          $scope.addNewEnvironment = function addNewEnvironment () {
            const newItemNo = $scope.envInfo.environments.length + 1;
            $scope.isFirst = false;
            $scope.envInfo.environments.push({"id": newItemNo});
          };
          $scope.removeEnvironment = function removeEnvironment (id) {
            const index = parseInt(id, 10);
            if ($scope.envInfo.environments.length > 1) {
              $scope.envInfo.environments.splice(index - 1, 1);
            }
            else {
              $scope.isFirst = true;
            }
          };
          $scope.ok = function ok () {
            $scope.envInfo.totalEnv = $scope.envInfo.environments.length;
            const inputValidations = angular.element(".environmentInput");
            let envValidation = true;
            let elem = 0;
            while (envValidation && inputValidations.length > elem) {
              if (angular.element(`#${inputValidations[elem].id}`).parsley().
                validate() === true) {
                envValidation = true;
              }
              else {
                envValidation = false;
              }
              elem += 1;
            }
            if (envValidation) {
              // Make the request
              const envReq = projectFtry2.addEnvironments(
                angular.toJson(angular.toJson($scope.envInfo)),
                data.project
              );
              // Capture the promise
              envReq.then((response) => {
                if (response.error) {
                  Rollbar.error("Error: An error occurred when " +
                              "adding a new environment");
                  $msg.error($translate.instant("proj_alerts.error_textsad"));
                }
                else {
                  const projt = descData.project.toUpperCase();
                  mixPanelDashboard.trackSearch(
                    "addEnvironment",
                    userEmail, projt
                  );
                  const respData = response.data.addEnvironments;
                  if (respData.success) {
                    const message = $translate.instant("search_findings" +
                                                  ".tab_resources.success");
                    const messageTitle = $translate.instant("search_findings" +
                                                  ".tab_users.title_success");
                    $msg.success(message, messageTitle);
                    const envs = respData.resources.environments;
                    $scope.$parent.envsDataset = angular.fromJson(envs);
                  }
                  else if (respData.access) {
                    Rollbar.error("Error: An error occurred when " +
                                "adding a new environment");
                    $msg.error($translate.instant("proj_alerts.error_textsad"));
                  }
                  else {
                    $msg.error($translate.instant("proj_alerts.access_denied"));
                  }
                  $uibModalInstance.close();
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
        "scope": $scope,
        "templateUrl": `${BASE.url}assets/views/project/addEnvironmentMdl.html`
      });
    };

    $scope.removeEnvironment = function removeEnvironment () {
      const selectedRow =
        angular.element("#tblEnvironments tr input:checked").closest("tr");
      if (selectedRow.length > 0) {
        const environments = {};
        environments.urlEnv = selectedRow.children()[1].textContent;
        const project = $stateParams.project.toLowerCase();
        const repo = projectFtry2.removeEnvironments(
          angular.toJson(angular.toJson(environments)),
          project
        );
        // Capture the promise
        repo.then((response) => {
          if (response.error) {
            Rollbar.error("Error: An error occurred when removing environment");
            $msg.error($translate.instant("proj_alerts.error_textsad"));
          }
          else {
            // Mixpanel tracking
            const projt = project.toUpperCase();
            mixPanelDashboard.trackSearch(
              "removeEnvironment",
              userEmail, projt
            );
            const respData = response.data.removeEnvironments;
            if (respData.success) {
              const message = $translate.instant("search_findings" +
                                            ".tab_resources.success_remove");
              const messageTitle = $translate.instant("search_findings" +
                                            ".tab_users.title_success");
              $msg.success(message, messageTitle);
              const envs = respData.resources.environments;
              $scope.envsDataset = angular.fromJson(envs);
            }
            else if (respData.access) {
              Rollbar.error("Error: An error occurred when " +
                          "removing environment");
              $msg.error($translate.instant("proj_alerts.error_textsad"));
            }
            else {
              $msg.error($translate.instant("proj_alerts.access_denied"));
            }
          }
        });
      }
      else {
        $msg.error($translate.instant("search_findings.tab_resources." +
                                  "no_selection"));
      }
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
