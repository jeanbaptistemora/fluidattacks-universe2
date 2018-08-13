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
            angular.forEach(usersData, (element) => {
              element.userRole = $translate.instant(`${"search_findings." +
                                            "tab_users."}${element.userRole}`);
              const DAYS_IN_MONTH = 30;
              if (element.usersLogin[0] >= DAYS_IN_MONTH) {
                const ROUNDED_MONTH = Math.round(element.usersLogin[0] /
                                               DAYS_IN_MONTH);
                element.usersLogin = ROUNDED_MONTH +
                                  $translate.instant("search_findings." +
                                                "tab_users.months_ago");
              }
              else if (element.usersLogin[0] > 0 &&
                       element.usersLogin[0] < DAYS_IN_MONTH) {
                element.usersLogin = element.usersLogin[0] +
                                  $translate.instant("search_findings." +
                                                "tab_users.days_ago");
              }
              else if (element.usersLogin[0] === -1) {
                element.usersLogin = "-";
                element.usersFirstLogin = "-";
              }
              else {
                const SECONDS_IN_HOUR = 3600;
                const ROUNDED_HOUR = Math.round(element.usersLogin[1] /
                                               SECONDS_IN_HOUR);
                const SECONDS_IN_MINUTES = 60;
                const ROUNDED_MINUTES = Math.round(element.usersLogin[1] /
                                                  SECONDS_IN_MINUTES);
                if (ROUNDED_HOUR >= 1 &&
                    ROUNDED_MINUTES >= SECONDS_IN_MINUTES) {
                  element.usersLogin = ROUNDED_HOUR +
                                $translate.instant("search_findings." +
                                              "tab_users.hours_ago");
                }
                else {
                  element.usersLogin = ROUNDED_MINUTES +
                                  $translate.instant("search_findings." +
                                                "tab_users.minutes_ago");
                }
              }
            });
            $scope.loadUsersInfo(projectName, vlang, usersData);
          }
          else if (response.error) {
            Rollbar.warning("Warning: Users not found");
            $msg.error($translate.instant("proj_alerts.error_textsad"));
          }
        });
      }
      return true;
    };

    $scope.loadUsersInfo = function loadUsersInfo (project, vlang, data) {
      // Eventuality table configuration

      angular.element("#tblUsers").bootstrapTable("destroy");
      angular.element("#tblUsers").bootstrapTable({
        "cookie": true,
        "cookieIdTable": "saveIdUser",
        data,
        "locale": vlang
      });
      angular.element("#tblUsers").bootstrapTable("refresh");
      angular.element("#tblUsers").bootstrapTable("hideColumn", "selection");
      if ($scope.isProjectManager || $scope.isAdmin) {
        angular.element("#tblUsers").bootstrapTable("showColumn", "selection");
      }
      angular.element("#search_section").show();
      angular.element("[data-toggle=\"tooltip\"]").tooltip();
    };

    $scope.addUser = function addUser () {
      // Obtener datos
      const descData = {"project": $stateParams.project.toLowerCase()};
      $uibModal.open({
        "animation": true,
        "backdrop": "static",
        "controller" ($scope, $uibModalInstance, data) {
          $scope.disableOnEdit = false;
          $scope.newUserInfo = {};
          $scope.isAdmin = userRole !== "customer" &&
                userRole !== "customeradmin" && userRole !== "analyst";
          const customerAdmin =
                    projectFtry2.isCustomerAdmin(data.project, userEmail);
          customerAdmin.then((response) => {
            if (!response.error) {
              $scope.isProjectManager = response.data;
            }
            else if (response.error) {
              $scope.isProjectManager = response.data;
            }
          });
          $scope.modalTitle = $translate.instant("search_findings." +
                                          "tab_users.title");
          $scope.newUserInfo.utilsUrl =
            `${BASE.url}assets/node_modules/intl-tel-input/build/js/utils.js`;
          $scope.ok = function ok () {
            if (angular.isUndefined($scope.newUserInfo.userPhone)) {
              $scope.newUserInfo.errorMessage = true;
            }
            else if (angular.element("#emailInput").parsley().
              validate() === true &&
                  angular.element("#organizationInput").parsley().
                    validate() === true &&
                    angular.element("#responsibilityInput").parsley().
                      validate() === true) {
              // Make the request
              const req = projectFtry.addAccessIntegrates(
                $scope.newUserInfo,
                data.project
              );
              // Capture the promise
              req.then((response) => {
                if (!response.error) {
                  // Mixpanel tracking
                  const projt = descData.project.toUpperCase();
                  mixPanelDashboard.trackUsersTab(
                    "AddUser",
                    userEmail,
                    projt,
                    "Add",
                    $scope.newUserInfo.userEmail
                  );
                  $msg.success(
                    $scope.newUserInfo.userEmail +
                    $translate.instant("search_findings.tab_users." +
                                                "success"),
                    $translate.instant("search_findings.tab_users." +
                                                "title_success")
                  );
                  $uibModalInstance.close();
                  location.reload();
                }
                else if (response.error) {
                  Rollbar.error("Error: An error occurred when " +
                              "adding a new user");
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
        "templateUrl": `${BASE.url}assets/views/project/adduserMdl.html`
      });
    };

    $scope.editUser = function editUser () {
      const adminEmail = [];
      let userOrganization = "";
      let userActualRole = "";
      let userResponsibility = "";
      let userPhone = "";
      angular.element("#tblUsers :checked").each(function checkedFields () {
        /* eslint-disable-next-line  no-invalid-this */
        const vm = this;
        const actualRow = angular.element("#tblUsers").find("tr");
        const actualIndex = angular.element(vm).data().index + 1;
        adminEmail.push(actualRow.eq(actualIndex)[0].cells[1].innerHTML);
        const INDEX_ROLE = 2;
        const INDEX_RESP = 3;
        const INDEX_PHONE = 4;
        const INDEX_ORG = 5;
        userActualRole =
          actualRow.eq(actualIndex)[0].cells[INDEX_ROLE].innerHTML;
        userResponsibility =
          actualRow.eq(actualIndex)[0].cells[INDEX_RESP].innerHTML;
        userPhone = actualRow.eq(actualIndex)[0].cells[INDEX_PHONE].innerHTML;
        userOrganization =
          actualRow.eq(actualIndex)[0].cells[INDEX_ORG].innerHTML;
      });
      if (adminEmail.length === 0) {
        $msg.error($translate.instant("search_findings.tab_users." +
                                  "no_selection"));
      }
      else if (adminEmail.length > 1) {
        $msg.error($translate.instant("search_findings.tab_users." +
                                    "assign_error"));
      }
      else {
        const descData = {
          "company": Organization.toLowerCase(),
          "project": $stateParams.project.toLowerCase()
        };
        $uibModal.open({
          "animation": true,
          "backdrop": "static",
          "controller" ($scope, $uibModalInstance, data) {
            $scope.newUserInfo = {};
            $scope.newUserInfo.userRole = userActualRole;
            $scope.newUserInfo.userResponsibility = userResponsibility;
            $scope.newUserInfo.userPhone = userPhone;
            $scope.newUserInfo.userOrganization = userOrganization;
            $scope.newUserInfo.userEmail = adminEmail[0].trim();
            $scope.disableOnEdit = true;
            $scope.isAdmin = userRole !== "customer" &&
                userRole !== "customeradmin" && userRole !== "analyst";
            const customerAdmin =
                        projectFtry2.isCustomerAdmin(data.project, userEmail);
            customerAdmin.then((response) => {
              if (!response.error) {
                $scope.isProjectManager = response.data;
              }
              else if (response.error) {
                $scope.isProjectManager = response.data;
              }
            });
            $scope.newUserInfo.utilsUrl =
              `${BASE.url}assets/node_modules/intl-tel-input/build/js/utils.js`;
            $scope.modalTitle = $translate.instant("search_findings." +
                                          "tab_users.edit_user_title");
            $scope.ok = function ok () {
              const re = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;
              if (angular.isUndefined($scope.newUserInfo.userPhone)) {
                $scope.newUserInfo.errorMessage = true;
              }
              else if (re.test(String($scope.newUserInfo.userEmail).
                toLowerCase()) &&
                  angular.element("#organizationInput").parsley().
                    validate() === true &&
                    angular.element("#responsibilityInput").parsley().
                      validate() === true) {
              // Make the request
                const req = projectFtry2.
                  editUser(
                    $scope.newUserInfo,
                    data.project
                  );
                // Capture the promise
                req.then((response) => {
                  if (!response.error) {
                  // Mixpanel tracking
                    mixPanelDashboard.trackUsersTab(
                      "EditUser",
                      userEmail,
                      $stateParams.project.toLowerCase(),
                      "EditUser",
                      adminEmail[0]
                    );
                    $msg.success(
                      $translate.instant("search_findings." +
                                           "tab_users.success_admin"),
                      $translate.instant("search_findings." +
                                                  "tab_users.title_success")
                    );
                    $uibModalInstance.close();
                    location.reload();
                  }
                  else if (response.error) {
                    Rollbar.error("Error: An error occurred " +
                                                "editing user information");
                    $msg.error($translate.instant("proj_alerts.error_textsad"));
                  }
                });
              }
              else {
                $msg.error($translate.instant("search_findings.tab_users." +
                                          "wrong_format"));
              }
            };
            $scope.close = function close () {
              $uibModalInstance.close();
            };
          },
          "keyboard": false,
          "resolve": {"data": descData},
          "templateUrl": `${BASE.url}assets/views/project/adduserMdl.html`
        });
      }
    };

    $scope.removeUserAccess = function removeUserAccess () {
      const removedEmails = [];
      angular.element("#tblUsers :checked").each(function checkedFields () {
        /* eslint-disable-next-line  no-invalid-this */
        const vm = this;
        const actualRow = angular.element("#tblUsers").find("tr");
        const actualIndex = angular.element(vm).data().index;
        if (angular.isUndefined(actualIndex)) {
          return true;
        }
        removedEmails.push(actualRow.eq(actualIndex + 1)[0].
          innerText.split("\t")[1]);
        return true;
      });
      if (removedEmails.length !== 0) {
        for (let inc = 0; inc < removedEmails.length; inc++) {
          const req = projectFtry2.removeAccessIntegrates(
            removedEmails[inc],
            $stateParams.project.toLowerCase()
          );
          req.then((response) => {
            if (!response.error) {
              mixPanelDashboard.trackUsersTab(
                "RemoveUser",
                userEmail,
                $stateParams.project.toLowerCase(),
                "Remove",
                removedEmails[inc]
              );
              $msg.success(removedEmails[inc] +
                               $translate.instant("search_findings.tab_users." +
                 "success_delete"), "search_findings.tab_users.title_success");
              if (inc === (removedEmails.length - 1)) {
                location.reload();
              }
            }
            else if (response.error) {
              Rollbar.error("Error: An error occurred " +
         "removing access to an user");
              $msg.error($translate.instant("proj_alerts.error_textsad"));
              inc = removedEmails.length;
              location.reload();
            }
          });
        }
      }
      else if (removedEmails.length === 0) {
        $msg.error($translate.instant("search_findings.tab_users." +
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
