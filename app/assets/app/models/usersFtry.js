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
      "editUser" ($scope) {
        const DATA_IN_SELECTED_ROW =
         angular.element("#tblUsers tr input:checked").closest("tr").
           children();

        if (angular.isUndefined(DATA_IN_SELECTED_ROW) ||
                                            DATA_IN_SELECTED_ROW.length === 0) {
          $msg.error($translate.instant("search_findings.tab_users." +
                                    "no_selection"));
        }
        else {
          const EMAIL_INDEX = 1;
          const ROLE_INDEX = 2;
          const RESPONSABILITY_INDEX = 3;
          const PHONE_INDEX = 4;
          const ORGANIZATION_INDEX = 5;

          const USER_EMAIL = DATA_IN_SELECTED_ROW[EMAIL_INDEX].textContent;
          const USER_ROLE = DATA_IN_SELECTED_ROW[ROLE_INDEX].textContent;
          const USER_RESPONSAILITY =
            DATA_IN_SELECTED_ROW[RESPONSABILITY_INDEX].textContent;
          const USER_PHONE = DATA_IN_SELECTED_ROW[PHONE_INDEX].textContent;
          const USER_ORGANIZATION =
            DATA_IN_SELECTED_ROW[ORGANIZATION_INDEX].textContent;
          const descData = {
            "company": Organization.toLowerCase(),
            "project": $scope.project.toLowerCase()
          };
          $uibModal.open({
            "animation": true,
            "backdrop": "static",
            "controller" ($scope, $uibModalInstance, data) {
              $scope.newUserInfo = {};
              $scope.newUserInfo.userRole = USER_ROLE;
              $scope.newUserInfo.userResponsibility = USER_RESPONSAILITY;
              $scope.newUserInfo.userPhone = USER_PHONE;
              $scope.newUserInfo.userOrganization = USER_ORGANIZATION;
              $scope.newUserInfo.userEmail = USER_EMAIL.trim();
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
                    if (response.error) {
                      Rollbar.error("Error: An error occurred " +
                                                  "editing user information");
                      $msg.error($translate.instant("proj_alerts." +
                                                    "error_textsad"));
                    }
                    else if (angular.isUndefined(response.data)) {
                      location.reload();
                    }
                    else if (response.data.editUser.access) {
                      if (response.data.editUser.success) {
                        // Mixpanel tracking
                        mixPanelDashboard.trackUsersTab(
                          "EditUser",
                          userEmail,
                          $stateParams.project.toLowerCase(),
                          "EditUser",
                          USER_EMAIL
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
                      else {
                        $msg.error($translate.instant("proj_alerts." +
                                                          "error_textsad"));
                      }
                    }
                    else {
                      $msg.error($translate.instant("proj_alerts." +
                                                        "access_denied"));
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
      }
    };
  }
);
