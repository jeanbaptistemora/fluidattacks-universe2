import { AxiosError, AxiosResponse } from "axios";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import { closeConfirmDialog } from "../../actions";
import * as actionTypes from "./actionTypes";

export interface IActionStructure {
  payload?: { [key: string]: string | string[] };
  type: string;
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

type ThunkResult<T> = ThunkAction<T, {}, undefined, IActionStructure>;

export const rejectDraft: ((draftId: string, projectName: string) => ThunkResult<void>) =
  (draftId: string, projectName: string): ThunkResult<void> =>
    (_0: ThunkDispatcher): void => {
      let gQry: string; gQry = `mutation {
        rejectDraft(findingId: "${draftId}") {
          success
        }
      }`;

      new Xhr().request(gQry, "An error occurred rejecting draft")
        .then((response: AxiosResponse) => {
          const { data } = response.data;

          if (data.rejectDraft.success) {
            msgSuccess(
              translate.t("search_findings.finding_rejected", { findingId: draftId }),
              translate.t("proj_alerts.title_success"));
            location.reload();
          }
        })
        .catch((error: AxiosError) => {
          if (error.response !== undefined) {
            const { errors } = error.response.data;

            switch (errors[0].message) {
              case "Exception - This draft has already been approved":
                msgError(translate.t("proj_alerts.draft_already_approved"));
                break;
              default:
                msgError(translate.t("proj_alerts.error_textsad"));
                rollbar.error(error.message, errors);
            }
          }
        });
    };

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

          dispatch(closeConfirmDialog("confirmDeleteFinding"));
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

export const approveDraft: ((draftId: string) => ThunkResult<void>) =
  (draftId: string): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string; gQry = `mutation {
        approveDraft(draftId: "${draftId}") {
          releaseDate
          success
        }
      }`;

      new Xhr().request(gQry, "An error occurred approving draft")
        .then((response: AxiosResponse) => {
          const { data } = response.data;

          if (data.approveDraft.success) {
            location.reload();
            msgSuccess(translate.t("search_findings.draft_approved"), translate.t("proj_alerts.title_success"));
          }
        })
        .catch((error: AxiosError) => {
          if (error.response !== undefined) {
            const { errors } = error.response.data;
            switch (errors[0].message) {
              case "Exception - This draft has already been approved":
                msgError(translate.t("proj_alerts.draft_already_approved"));
                break;
              case "CANT_APPROVE_FINDING_WITHOUT_VULNS":
                msgError(translate.t("proj_alerts.draft_without_vulns"));
                break;
              default:
                msgError(translate.t("proj_alerts.error_textsad"));
                rollbar.error(error.message, errors);
            }
          }
        });
    };

export const clearFindingState: (() => IActionStructure) = (): IActionStructure => ({
  type: actionTypes.CLEAR_FINDING_STATE,
});
