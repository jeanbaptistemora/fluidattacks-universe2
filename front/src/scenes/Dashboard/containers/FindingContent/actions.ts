import { AxiosError, AxiosResponse } from "axios";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError, msgSuccess } from "../../../../utils/notifications";
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

export const deleteFinding: ((findingId: string, projectName: string, justification: string) => ThunkResult<void>) =
  (findingId: string, projectName: string, justification: string): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string; gQry = `mutation {
        deleteFinding(findingId: "${findingId}", justification: ${justification}) {
          success
        }
      }`;

      new Xhr().request(gQry, "An error occurred deleting finding")
        .then((response: AxiosResponse) => {
          const { data } = response.data;

          if (data.deleteFinding.success) {
            msgSuccess(
              translate.t("search_findings.finding_deleted", { findingId }),
              translate.t("proj_alerts.title_success"));
            location.hash = `#!/project/${projectName}/findings`;
            location.reload();
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
