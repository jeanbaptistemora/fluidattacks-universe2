import { AxiosError, AxiosResponse } from "axios";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import * as actionTypes from "./actionTypes";

export interface IActionStructure {
  payload?: { [key: string]: string | string[] };
  type: string;
}

export type ThunkDispatcher = ThunkDispatch<{}, {}, IActionStructure>;

type ThunkResult<T> = ThunkAction<T, {}, {}, IActionStructure>;

export const clearProjectState: (() => IActionStructure) = (): IActionStructure => ({
  type: actionTypes.CLEAR_PROJECT_STATE,
});

export const loadProjectData: ((projectName: string) => ThunkResult<void>) =
  (projectName: string): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string; gQry = `{
        me {
          role(projectName: "${projectName}")
        }
      }`;

      new Xhr().request(gQry, "An error occurred getting project data")
        .then((response: AxiosResponse) => {
          const { data } = response.data;

          dispatch({ payload: { role: data.me.role }, type: actionTypes.LOAD_PROJECT });
        })
        .catch((error: AxiosError) => {
          if (error.response !== undefined) {
            const { errors } = error.response.data;

            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error(error.message, errors);
          }
        });
    };
