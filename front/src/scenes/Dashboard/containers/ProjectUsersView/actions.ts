import { AxiosError, AxiosResponse } from "axios";
import { reset } from "redux-form";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { formatUserlist } from "../../../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import { IDashboardState } from "../../reducer";
import * as actionTypes from "./actionTypes";

type IUserData = IDashboardState["users"]["userList"][0];

export interface IActionStructure {
  payload?: { [key: string]: string | string[] | ({} | undefined) };
  type: string;
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

type ThunkResult<T> = ThunkAction<T, {}, undefined, IActionStructure>;

export const loadUsers: ((projectName: string) => ThunkResult<void>) = (projectName: string): ThunkResult<void> =>
  (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `{
      project(projectName:"${projectName}"){
        users {
          email
          role
          responsibility
          phoneNumber
          organization
          firstLogin
          lastLogin
        }
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting project users")
      .then((response: AxiosResponse) => {
        const { data } = response.data;

        dispatch({
          payload: { userlist: formatUserlist(data.project.users) },
          type: actionTypes.LOAD_USERS,
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

export const openUsersMdl: ((type: "add" | "edit", initialValues?: {}) => IActionStructure) =
  (type: "add" | "edit", initialValues?: {}): IActionStructure => ({
    payload: { type, initialValues },
    type: actionTypes.OPEN_USERS_MDL,
  });

export const closeUsersMdl: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_USERS_MDL,
  });

export const editUser: ((modifiedUser: IUserData, projectName: string) => ThunkResult<void>) =
  (modifiedUser: IUserData, projectName: string): ThunkResult<void> => (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
       editUser(
         projectName: "${projectName}",
         email: "${modifiedUser.email}",
         organization: "${modifiedUser.organization}",
         phoneNumber: "${modifiedUser.phoneNumber}",
         responsibility: "${modifiedUser.responsibility}",
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

export const removeUser: ((projectName: string, email: string) => ThunkResult<void>) =
  (projectName: string, email: string): ThunkResult<void> => (dispatch: ThunkDispatcher): void => {
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
            type: actionTypes.REMOVE_USER,
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

export const addUser: ((newUser: IUserData, projectName: string) => ThunkResult<void>) =
  (newUser: IUserData, projectName: string): ThunkResult<void> => (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
     grantUserAccess(
       email: "${newUser.email}",
       organization: "${newUser.organization}",
       phoneNumber: "${newUser.phoneNumber}",
       projectName: "${projectName}",
       responsibility: "${newUser.responsibility}",
       role: "${newUser.role}"
     ) {
       success
       grantedUser {
         email
         role
         responsibility
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
            type: actionTypes.ADD_USER,
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
