/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */
import { AxiosError, AxiosResponse } from "axios";
import { Action, AnyAction, Dispatch } from "redux";
import { reset } from "redux-form";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { formatUserlist } from "../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../utils/notifications";
import rollbar from "../../utils/rollbar";
import translate from "../../utils/translations/translate";
import Xhr from "../../utils/xhr";
import * as actionType from "./actionTypes";
import { IProjectUsersViewProps, IUserData } from "./components/ProjectUsersView/index";
import { IRecordsViewProps } from "./components/RecordsView";
import { IVulnerabilitiesViewProps } from "./components/Vulnerabilities/index";

export interface IActionStructure {
  payload: any;
  type: string;
}

type DashboardAction = ((...args: any[]) => IActionStructure);
type ThunkDispatcher = Dispatch<Action> & ThunkDispatch<{}, {}, AnyAction>;
type ThunkActionStructure = ((...args: any[]) => ThunkAction<void, {}, {}, AnyAction>);

export const loadResources: DashboardAction =
  (repos: Array<{ branch: string; urlRepo: string }>,
   envs: Array<{ urlEnv: string }>): IActionStructure => ({
    payload: {
      environments: envs,
      repositories: repos,
    },
    type: actionType.LOAD_RESOURCES,
});

export const clearResources: DashboardAction =
  (): IActionStructure => ({
  payload: undefined,
  type: actionType.CLEAR_RESOURCES,
});

export const addRepositoryField: DashboardAction =
  (): IActionStructure => ({
      payload: undefined,
      type: actionType.ADD_REPO_FIELD,
});

export const removeRepositoryField: DashboardAction =
  (index: number): IActionStructure => ({
      payload: { index },
      type: actionType.REMOVE_REPO_FIELD,
});

export const addEnvironmentField: DashboardAction =
  (): IActionStructure => ({
      payload: undefined,
      type: actionType.ADD_ENV_FIELD,
});

export const removeEnvironmentField: DashboardAction =
  (index: number): IActionStructure => ({
      payload: { index },
      type: actionType.REMOVE_ENV_FIELD,
});

export const openAddModal: DashboardAction =
  (type: "repository" | "environment"): IActionStructure => ({
      payload: { type },
      type: actionType.OPEN_ADD_MODAL,
});

export const closeAddModal: DashboardAction =
  (): IActionStructure => ({
      payload: undefined,
      type: actionType.CLOSE_ADD_MODAL,
});

export const modifyRepoUrl: DashboardAction =
  (index: number, newValue: string): IActionStructure => ({
      payload: {
        index,
        newValue,
      },
      type: actionType.MODIFY_REPO_URL,
});

export const modifyRepoBranch: DashboardAction =
  (index: number, newValue: string): IActionStructure => ({
      payload: {
        index,
        newValue,
      },
      type: actionType.MODIFY_REPO_BRANCH,
});

export const modifyEnvUrl: DashboardAction =
  (index: number, newValue: string): IActionStructure => ({
      payload: {
        index,
        newValue,
      },
      type: actionType.MODIFY_ENV_URL,
});

export const addFileName: DashboardAction =
  (newValue: string): IActionStructure => ({
      payload: {
        newValue,
      },
      type: actionType.ADD_FILE_NAME,
});

export const clearUsers: DashboardAction =
  (): IActionStructure => ({
  payload: undefined,
  type: actionType.CLEAR_USERS,
});

export const loadUsers: ThunkActionStructure =
  (
    projectName: IProjectUsersViewProps["projectName"],
  ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
    dispatch(clearUsers());
    let gQry: string;
    gQry = `{
      projectUsers(projectName:"${projectName}"){
        email
        role
        responsability
        phoneNumber
        organization
        firstLogin
        lastLogin
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting project users")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      dispatch({
          payload: { userlist: formatUserlist(data.projectUsers) },
          type: actionType.LOAD_USERS,
      });
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const removeUser: ThunkActionStructure =
  (
    projectName: IProjectUsersViewProps["projectName"],
    email: IUserData["email"],
  ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      removeUserAccess(projectName: "${projectName}", userEmail: "${email}"){
        removedEmail
        success
      }
    }`;
    new Xhr().request(gQry, "An error occurred removing users")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      if (data.removeUserAccess.success) {
        const removedEmail: string = data.removeUserAccess.removedEmail;

        dispatch({
          payload: { removedEmail },
          type: actionType.REMOVE_USER,
        });
        msgSuccess(
          `${email} ${translate.t("search_findings.tab_users.success_delete")}`,
          translate.t("search_findings.tab_users.title_success"),
        );
      } else {
        msgError(translate.t("proj_alerts.error_textsad"));
      }
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const openUsersMdl: DashboardAction =
  (type: "add" | "edit", initialValues?: {}): IActionStructure => ({
    payload: { type, initialValues },
    type: actionType.OPEN_USERS_MDL,
});

export const closeUsersMdl: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.CLOSE_USERS_MDL,
});

export const addUser: ThunkActionStructure =
 (
   newUser: IUserData,
   projectName: IProjectUsersViewProps["projectName"],
 ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
   let gQry: string;
   gQry = `mutation {
     grantUserAccess(
       email: "${newUser.email}",
       organization: "${newUser.organization}",
       phoneNumber: "${newUser.phone}",
       projectName: "${projectName}",
       responsibility: "${newUser.responsability}",
       role: "${newUser.role}"
     ) {
       success
       grantedUser {
         email
         role
         responsability
         phoneNumber
         organization
         firstLogin
         lastLogin
       }
     }
   }`;
   new Xhr().request(gQry, "An error occurred adding user to project")
   .then((response: AxiosResponse) => {
     const { data } = response.data;

     if (data.grantUserAccess.success) {
       msgSuccess(
         `${newUser.email}${translate.t("search_findings.tab_users.success")}`,
         translate.t("search_findings.tab_users.title_success"),
       );
       dispatch(reset("addUser"));
       dispatch(closeUsersMdl());
       dispatch({
         payload: { newUser: formatUserlist([data.grantUserAccess.grantedUser])[0] },
         type: actionType.ADD_USER,
       });
     } else {
       msgError(translate.t("proj_alerts.error_textsad"));
     }
   })
   .catch((error: AxiosError) => {
     if (error.response !== undefined) {
       const { errors } = error.response.data;

       msgError(translate.t("proj_alerts.error_textsad"));
       rollbar.error(error.message, errors);
     }
   });
};

export const loadVulnerabilities: DashboardAction =
  (dataInputs: IVulnerabilitiesViewProps["dataInputs"],
   dataLines: IVulnerabilitiesViewProps["dataLines"],
   dataPorts: IVulnerabilitiesViewProps["dataPorts"]): IActionStructure => ({
    payload: {
      dataInputs,
      dataLines,
      dataPorts,
    },
    type: actionType.LOAD_VULNERABILITIES,
});

export const editUser: ThunkActionStructure =
 (
   modifiedUser: IUserData,
   projectName: IProjectUsersViewProps["projectName"],
 ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
   let gQry: string;
   gQry = `mutation {
     editUser(
       projectName: "${projectName}",
       email: "${modifiedUser.email}",
       organization: "${modifiedUser.organization}",
       phoneNumber: "${modifiedUser.phone}",
       responsibility: "${modifiedUser.responsability}",
       role: "${modifiedUser.role}"
     ) {
       success
     }
   }`;
   new Xhr().request(gQry, "An error occurred editing user information")
   .then((response: AxiosResponse) => {
     const { data } = response.data;

     if (data.editUser.success) {
       msgSuccess(
         translate.t("search_findings.tab_users.success_admin"),
         translate.t("search_findings.tab_users.title_success"),
       );
       dispatch(reset("addUser"));
       dispatch(closeUsersMdl());
       location.reload();
     } else {
       msgError(translate.t("proj_alerts.error_textsad"));
     }
   })
   .catch((error: AxiosError) => {
     if (error.response !== undefined) {
       const { errors } = error.response.data;

       msgError(translate.t("proj_alerts.error_textsad"));
       rollbar.error(error.message, errors);
     }
   });
};

export const loadRecords: ThunkActionStructure =
(
  findingId: IRecordsViewProps["findingId"],
): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
  let gQry: string;
  gQry = `{
    finding(identifier: "${findingId}") {
      records
    }
  }`;
  new Xhr().request(gQry, "An error occurred getting compromised records")
  .then((response: AxiosResponse) => {
    const { data } = response.data;
    dispatch({
      payload: { records: JSON.parse(data.finding.records) },
      type: actionType.LOAD_RECORDS,
    });
  })
  .catch((error: AxiosError) => {
    if (error.response !== undefined) {
      const { errors } = error.response.data;

      msgError("There was an error :(");
      rollbar.error(error.message, errors);
    }
  });
};

export const editRecords: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.EDIT_RECORDS,
});
