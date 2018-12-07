import { AxiosError, AxiosResponse } from "axios";
import { Action, AnyAction, Dispatch } from "redux";
import { reset } from "redux-form";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { formatUserlist } from "../../../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import * as actionTypes from "./actionTypes";
import { IProjectUsersViewProps, IUserData } from "./index";

export interface IActionStructure {
  /* tslint:disable-next-line:no-any
   * Disabling this rule is necessary because the payload
   * type may differ between actions
   */
  payload: any;
  type: string;
}

type ThunkDispatcher = Dispatch<Action> & ThunkDispatch<{}, {}, AnyAction>;
/* tslint:disable-next-line:no-any
 * Disabling this rule is necessary because the args
 * of an async action may differ
 */
type ThunkActionStructure = ((...args: any[]) => ThunkAction<void, {}, {}, AnyAction>);

export const clearUsers: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLEAR_USERS,
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
