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

export const loadFindingsData: ((projectName: string) => ThunkResult<void>) =
  (projectName: string): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string; gQry = `{
        project(projectName: "${projectName}") {
          drafts {
            id
            reportDate
            type
            title
            description
            severityScore
            openVulnerabilities
            isExploitable
            releaseDate
          }
        }
      }`;

      new Xhr().request(gQry, "An error occurred getting project drafts")
        .then((response: AxiosResponse) => {
          const { data } = response.data;

          dispatch({
            payload: {
              dataset: data.project.drafts,
            },
            type: actionTypes.LOAD_DRAFTS,
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
