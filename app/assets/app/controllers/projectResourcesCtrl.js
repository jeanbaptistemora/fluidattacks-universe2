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
        const reqResources = projectFtry2.resourcesByProject(projectName);
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
          else {
            const respData = response.data;
            if (angular.isUndefined(respData)) {
              location.reload();
            }
            else {
              $scope.view.project = true;
              const projectRepoInfo =
                              angular.fromJson(respData.resources.repositories);
              $scope.loadRepoInfo(projectName, projectRepoInfo);
              const projectEnvInfo =
                              angular.fromJson(respData.resources.environments);
              $scope.loadEnvironmentInfo(projectName, projectEnvInfo);
            }
          }
        });
      }
      return true;
    };

    $scope.loadRepoInfo = function loadRepoInfo (project, data) {
      // Resources tables configuration
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
      angular.element("#tblRepositories").bootstrapTable("destroy");
      angular.element("#tblRepositories").bootstrapTable({
        "cookie": true,
        "cookieIdTable": "saveIdRepositories",
        data,
        "locale": vlang
      });
      angular.element("#tblRepositories").bootstrapTable("refresh");
      angular.element("#search_section").show();
      angular.element("[data-toggle=\"tooltip\"]").tooltip();
    };

    $scope.loadEnvironmentInfo = function loadEnvironmentInfo (project, data) {
      let vlang = "en-US";
      if (localStorage.lang === "en") {
        vlang = "en-US";
      }
      else {
        vlang = "es-CO";
      }
      angular.element("#tblEnvironments").bootstrapTable("destroy");
      angular.element("#tblEnvironments").bootstrapTable({
        "cookie": true,
        "cookieIdTable": "saveIdEnvironments",
        data,
        "locale": vlang
      });
      angular.element("#tblEnvironments").bootstrapTable("refresh");
      angular.element("#search_section").show();
      angular.element("[data-toggle=\"tooltip\"]").tooltip();
    };

    $scope.removeRepository = function removeRepository () {
      let repository = "";
      let branch = "";
      angular.element("#tblRepositories :checked").
        each(function checkedFields () {
          /* eslint-disable-next-line  no-invalid-this */
          const vm = this;
          const actualRow = angular.element("#tblRepositories").find("tr");
          const actualIndex = angular.element(vm).data().index + 1;
          const INDEX_BRANCH = 2;
          repository = actualRow.eq(actualIndex)[0].cells[1].innerHTML;
          branch =
            actualRow.eq(actualIndex)[0].cells[INDEX_BRANCH].innerHTML;
        });
      if (repository.length === 0) {
        $msg.error($translate.instant("search_findings.tab_resources." +
                                  "no_selection"));
      }
      else {
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
            const respData = response.data;
            // Mixpanel tracking
            const projt = project.toUpperCase();
            mixPanelDashboard.trackSearch(
              "removeRepository",
              userEmail,
              projt
            );

            if (respData.removeRepositories.success) {
              const message = $translate.instant("search_findings" +
                                            ".tab_resources.success_remove");
              const messageTitle = $translate.instant("search_findings" +
                                            ".tab_users.title_success");
              $msg.success(message, messageTitle);
              const repos = respData.removeRepositories.
                resources.repositories;
              $scope.loadRepoInfo(projt, angular.fromJson(repos));
            }
            else {
              Rollbar.error("Error: An error occurred when removing " +
                            "repository");
              $msg.error($translate.instant("proj_alerts.error_textsad"));
            }
          }
        });
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
                  const respData = response.data;
                  // Mixpanel tracking
                  const projt = descData.project.toUpperCase();
                  mixPanelDashboard.trackSearch(
                    "addRepository",
                    userEmail,
                    projt
                  );
                  if (respData.addRepositories.success) {
                    const message = $translate.instant("search_findings" +
                                                  ".tab_resources.success");
                    const messageTitle = $translate.instant("search_findings" +
                                                  ".tab_users.title_success");
                    $msg.success(message, messageTitle);
                    const repos = respData.addRepositories.
                      resources.repositories;
                    $scope.loadRepoInfo(projt, angular.fromJson(repos));
                  }
                  else {
                    $msg.error($translate.instant("proj_alerts.error_textsad"));
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
      // Obtener datos
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
                $scope.envInfo,
                data.project
              );
              // Capture the promise
              envReq.then((response) => {
                if (!response.error) {
                  // Mixpanel tracking
                  const projt = descData.project.toUpperCase();
                  mixPanelDashboard.trackSearch(
                    "addEnvironment",
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
                              "adding a new environment");
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
        "templateUrl": `${BASE.url}assets/views/project/addEnvironmentMdl.html`
      });
    };

    $scope.removeEnvironment = function removeEnvironment () {
      let environment = "";
      angular.element("#tblEnvironments :checked").
        each(function checkedFields () {
          /* eslint-disable-next-line  no-invalid-this */
          const vm = this;
          const actualRow = angular.element("#tblEnvironments").find("tr");
          const actualIndex = angular.element(vm).data().index + 1;
          environment = actualRow.eq(actualIndex)[0].cells[1].innerHTML;
        });
      if (environment.length === 0) {
        $msg.error($translate.instant("search_findings.tab_resources." +
                                  "no_selection"));
      }
      else {
        const environments = {};
        environments.urlEnv = environment;
        const project = $stateParams.project.toLowerCase();
        const repo = projectFtry2.removeEnvironments(
          environments,
          project
        );
        // Capture the promise
        repo.then((response) => {
          if (!response.error) {
            // Mixpanel tracking
            const projt = project.toUpperCase();
            mixPanelDashboard.trackSearch(
              "removeEnvironment",
              userEmail,
              projt
            );
            const message = $translate.instant("search_findings" +
                                          ".tab_resources.success_remove");
            const messageTitle = $translate.instant("search_findings" +
                                          ".tab_users.title_success");
            $msg.success(message, messageTitle);
            location.reload();
          }
          else if (response.error) {
            Rollbar.error("Error: An error occurred when " +
                        "removing environment");
            $msg.error($translate.instant("proj_alerts.error_textsad"));
          }
        });
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
