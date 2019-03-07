import { AxiosError, AxiosResponse } from "axios";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import { calcCVSS } from "../SeverityView/actions";
import * as actionTypes from "./actionTypes";

export interface IActionStructure {
  payload?: Map<string, string>;
  type: string;
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

type ThunkResult<T> = ThunkAction<T, {}, undefined, IActionStructure>;

export const loadFindingData: ((findingId: string) => ThunkResult<void>) =
  (findingId: string): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string; gQry = `{
        finding(identifier: "${findingId}") {
          severity
          state
          openVulnerabilities
          releaseDate
          cvssVersion
        }
      }`;

      new Xhr().request(gQry, "An error occurred getting finding header data")
        .then((response: AxiosResponse) => {
          const { data } = response.data;

          dispatch({
            payload: {
              openVulns: data.finding.openVulnerabilities,
              reportDate: data.finding.releaseDate.split(" ")[0],
              status: data.finding.state,
            },
            type: actionTypes.LOAD_FINDING,
          });
          dispatch(calcCVSS(data.finding.severity, data.finding.cvssVersion));
        })
        .catch((error: AxiosError) => {
          if (error.response !== undefined) {
            const { errors } = error.response.data;

            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error(error.message, errors);
          }
        });
    };

export const rejectDraft: ((draftId: string, projectName: string) => ThunkResult<void>) =
  (draftId: string, projectName: string): ThunkResult<void> =>
    (_0: ThunkDispatcher): void => {
      let gQry: string; gQry = `mutation {
        rejectDraft(draftId: "${draftId}") {
          success
        }
      }`;

      new Xhr().request(gQry, "An error occurred rejecting draft")
        .then((response: AxiosResponse) => {
          const { data } = response.data;

          if (data.rejectDraft.success) {
            location.hash = `#!/project/${projectName}/drafts`;
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

export const clearFindingState: (() => IActionStructure) = (): IActionStructure => ({
  type: actionTypes.CLEAR_FINDING_STATE,
});
