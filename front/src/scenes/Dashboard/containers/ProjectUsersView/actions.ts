import { AxiosError, AxiosResponse } from "axios";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { formatUserlist } from "../../../../utils/formatHelpers";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import * as actionTypes from "./actionTypes";

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
