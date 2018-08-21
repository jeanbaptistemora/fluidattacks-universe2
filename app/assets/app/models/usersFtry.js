/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,1] }]*/
/* global integrates, BASE, $xhr, response:true, Organization, angular,
mixPanelDashboard,$msg, $, Rollbar, userRole, draftData:true,
projectData: true, userEmail, userName */
/* eslint no-shadow: ["error", { "allow": ["$scope","$stateParams",
                                          "response"] }]*/
/**
 * @file usersFtry.js
 * @author engineering@fluidattacks.com
 */
/**
 * Factory definition for the 1st set of auxiliar functions.
 * @name usersFtry
 * @param {Object} $q Angular constructor
 * @param {Object} $translate Angular translator
 * @param {Object} projectFtry2 Factory with main functions
 * @return {undefined}
 */
/** @export */
angular.module("FluidIntegrates").factory(
  "usersFtry",
  function usersFtry (
    $stateParams,
    $timeout,
    $translate,
    $uibModal,
    projectFtry,
    projectFtry2
  ) {
    return {
      "addUser" ($scope) {
        // Obtener datos
        const descData = {"project": $scope.project.toLowerCase()};
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
      },
      "editUser" ($scope) {
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
            "project": $scope.project.toLowerCase()
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
              $scope.newUserInfo.utilsUrl = `${BASE.url}assets/node_modules/
                intl-tel-input/build/js/utils.js`;
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
                      const errorMsg =
                        $translate.instant("proj_alerts.error_textsad");
                      $msg.error(errorMsg);
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
      },
      "removeUserAccess" ($scope) {
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
                  $scope.project.toLowerCase(),
                  "Remove",
                  removedEmails[inc]
                );
                const removedMsg = removedEmails[inc] +
                  $translate.instant("search_findings.tab_users." +
                    "success_delete");
                const titleMsg =
                  $translate.instant("search_findings.tab_users.title_success");
                $msg.success(removedMsg, titleMsg);
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
      }
    };
  }
);
