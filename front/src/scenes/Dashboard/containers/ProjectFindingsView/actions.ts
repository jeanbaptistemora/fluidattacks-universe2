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

export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

type ThunkResult<T> = ThunkAction<T, {}, undefined, IActionStructure>;

export const openReportsModal: (() => IActionStructure) = (): IActionStructure => ({
  type: actionTypes.OPEN_REPORTS_MODAL,
});

export const closeReportsModal: (() => IActionStructure) = (): IActionStructure => ({
  type: actionTypes.CLOSE_REPORTS_MODAL,
});

export const loadFindingsData: ((projectName: string) => ThunkResult<void>) =
  (projectName: string): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string; gQry = `{
        project(projectName: "${projectName}") {
          findings {
            id
          	age
            lastVulnerability
            type
            title
            description
            severityScore
            openVulnerabilities
            state
            treatment
            isExploitable
          }
          hasCompleteDocs
        }
      }`;

      new Xhr().request(gQry, "An error occurred getting project findings")
        .then((response: AxiosResponse) => {
          const { data } = response.data;

          dispatch({
            payload: {
              dataset: data.project.findings,
              hasExecutive: data.project.hasCompleteDocs,
            },
            type: actionTypes.LOAD_FINDINGS,
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
