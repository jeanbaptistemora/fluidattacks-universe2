import { AxiosError, AxiosResponse } from "axios";
import { Action, AnyAction, Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import * as actionTypes from "./actionTypes";

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

export const openEvidence: ((imgIndex: number) => IActionStructure) =
  (imgIndex: number): IActionStructure => ({
    payload: { imgIndex },
    type: actionTypes.OPEN_EVIDENCE,
  });

export const closeEvidence: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_EVIDENCE,
  });

export const moveEvidenceIndex:
  ((currentIndex: number, totalImages: number, direction: "next" | "previous") => IActionStructure) =
  (currentIndex: number, totalImages: number, direction: "next" | "previous"): IActionStructure => ({
    payload: {
      index: (direction === "next" ? (currentIndex + 1) : (currentIndex + totalImages - 1))
        % totalImages,
    },
    type: actionTypes.MOVE_EVIDENCE,
  });

export const editEvidence: ((value: boolean) => IActionStructure) =
  (value: boolean): IActionStructure => ({
    payload: { value },
    type: actionTypes.EDIT_EVIDENCE,
  });

export const clearEvidence: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLEAR_EVIDENCE,
  });

export const loadEvidence: ThunkActionStructure =
  (findingId: string): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `{
        finding(identifier: "${findingId}") {
          evidence
        }
      }`;
    new Xhr().request(gQry, "An error occurred getting evidence")
      .then((response: AxiosResponse) => {
        const { data } = response.data;

        dispatch({
          payload: {
            images: [
              {
                description: translate.t("search_findings.tab_evidence.animation_exploit"),
                url: data.finding.evidence.animation.url,
              },
              {
                description: translate.t("search_findings.tab_evidence.evidence_exploit"),
                url: data.finding.evidence.exploitation.url,
              },
              data.finding.evidence.evidence1,
              data.finding.evidence.evidence2,
              data.finding.evidence.evidence3,
              data.finding.evidence.evidence4,
              data.finding.evidence.evidence5,
            ],
          },
          type: actionTypes.LOAD_EVIDENCE,
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

export const updateEvidenceDescription: ThunkActionStructure =
(
  value: string, findingId: string, field: string,
): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
  let gQry: string;
  gQry = `mutation {
        updateDescription: updateEvidenceDescription (
          description: ${JSON.stringify(value)},
          findingId: "${findingId}",
          field: "${field}") {
          success
          finding {
            evidence
          }
        }
      }`;
  new Xhr().request(gQry, "An error occurred updating evidence")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      if (data.updateDescription.success) {
        dispatch({
          payload: {
            images: [
              {
                description: translate.t("search_findings.tab_evidence.animation_exploit"),
                url: data.updateDescription.finding.evidence.animation.url,
              },
              {
                description: translate.t("search_findings.tab_evidence.evidence_exploit"),
                url: data.updateDescription.finding.evidence.exploitation.url,
              },
              data.updateDescription.finding.evidence.evidence1,
              data.updateDescription.finding.evidence.evidence2,
              data.updateDescription.finding.evidence.evidence3,
              data.updateDescription.finding.evidence.evidence4,
              data.updateDescription.finding.evidence.evidence5,
            ],
          },
          type: actionTypes.LOAD_EVIDENCE,
        });
        dispatch(editEvidence(false));
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

export const updateEvidence: ThunkActionStructure =
  (
    findingId: string, evidenceId: number, value: string, field: string,
  ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
        updateEvidence (
          evidenceId: "${evidenceId}",
          findingId: "${findingId}", file: "") {
          success
          finding {
            evidence
          }
        }
      }`;
    new Xhr().upload(gQry, `#evidence${evidenceId}`, "An error occurred updating evidence")
      .then((response: AxiosResponse) => {
        const { data } = response.data;

        if (data.updateEvidence.success) {
          dispatch({
            payload: {
              images: [
                {
                  description: translate.t("search_findings.tab_evidence.animation_exploit"),
                  url: data.updateEvidence.finding.evidence.animation.url,
                },
                {
                  description: translate.t("search_findings.tab_evidence.evidence_exploit"),
                  url: data.updateEvidence.finding.evidence.exploitation.url,
                },
                data.updateEvidence.finding.evidence.evidence1,
                data.updateEvidence.finding.evidence.evidence2,
                data.updateEvidence.finding.evidence.evidence3,
                data.updateEvidence.finding.evidence.evidence4,
                data.updateEvidence.finding.evidence.evidence5,
              ],
            },
            type: actionTypes.LOAD_EVIDENCE,
          });
          if (evidenceId > 1) {
            dispatch(updateEvidenceDescription(value, findingId, field));
          }
          dispatch(editEvidence(false));
        } else {
          msgError(translate.t("proj_alerts.error_textsad"));
        }
      })
      .catch((error: AxiosError) => {
        if (error.response !== undefined) {
          const { errors } = error.response.data;

          switch (errors[0].message) {
            case "File exceeds the size limits":
              msgError(translate.t("proj_alerts.file_size"));
              break;
            case "Extension not allowed":
              msgError(translate.t("proj_alerts.file_type_wrong"));
              break;
            default:
              msgError(translate.t("proj_alerts.no_file_update"));
              rollbar.error(error.message, errors);
          }
        }
      });
  };
