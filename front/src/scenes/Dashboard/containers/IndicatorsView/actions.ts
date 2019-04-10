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

export const loadIndicators: ((projectName: string) => ThunkResult<void>) =
  (projectName: string): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `{
        project(projectName: "${projectName}"){
          closedVulnerabilities
          currentMonthAuthors
          currentMonthCommits
          lastClosingVuln
          maxOpenSeverity
          maxSeverity
          meanRemediate
          openVulnerabilities
          pendingClosingCheck
          totalFindings
          totalTreatment
        }
        resources(projectName: "${projectName}"){
          repositories
        }
      }`;
      new Xhr().request(gQry, "An error occurred getting tags")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          dispatch({
            payload: {
              closedVulnerabilities: data.project.closedVulnerabilities,
              currentMonthAuthors: data.project.currentMonthAuthors,
              currentMonthCommits: data.project.currentMonthCommits,
              lastClosingVuln: data.project.lastClosingVuln,
              maxOpenSeverity: data.project.maxOpenSeverity,
              maxSeverity: data.project.maxSeverity,
              meanRemediate: data.project.meanRemediate,
              openVulnerabilities: data.project.openVulnerabilities,
              pendingClosingCheck: data.project.pendingClosingCheck,
              repositories: JSON.parse(data.resources.repositories),
              totalFindings: data.project.totalFindings,
              totalTreatment: data.project.totalTreatment,
            },
            type: actionTypes.LOAD_INDICATORS,
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
