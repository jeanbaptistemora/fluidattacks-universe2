import { AxiosError, AxiosResponse } from "axios";
import { Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError, msgSuccess } from "../../../../utils/notifications";
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

type ThunkDispatcher = Dispatch<IActionStructure> & ThunkDispatch<{}, {}, IActionStructure>;
/* tslint:disable-next-line:no-any
 * Disabling this rule is necessary because the args
 * of an async action may differ
 */
type ThunkActionStructure<T> = ((...args: any[]) => ThunkAction<T, {}, {}, IActionStructure>);

export const editDescription: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.EDIT_DESCRIPTION,
  });

export const openRemediationMdl: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.OPEN_REMEDIATION_MDL,
  });

export const closeRemediationMdl: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_REMEDIATION_MDL,
  });

export const openConfirmMdl: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.OPEN_CONFIRM_MDL,
  });

export const closeConfirmMdl: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_CONFIRM_MDL,
  });

export const loadDescription: ThunkActionStructure<void> =
  (findingId: string, projectName: string): ThunkAction<void, {}, {}, IActionStructure> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `{
        project(projectName: "${projectName}") {
          subscription
        }
        finding(identifier: "${findingId}") {
          reportLevel
          title
          scenario
          actor
          description
          requirements
          attackVector
          threat
          recommendation
          releaseDate
          remediated
          state
          affectedSystems
          compromisedAttributes
          compromisedRecords
          cweUrl
          btsUrl
          treatment
          treatmentManager
          treatmentJustification
        }
      }`;

      new Xhr().request(gQry, "An error occurred getting finding description")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          dispatch<IActionStructure>({
            payload: {
              descriptionData: { ...data.finding, ...data.project },
            },
            type: actionTypes.LOAD_DESCRIPTION,
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

export const requestVerification: ThunkActionStructure<void> =
  (findingId: string, justification: string): ThunkAction<void, {}, {}, IActionStructure> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `mutation {
        requestVerification(
          findingId: "${findingId}",
          justification: ${JSON.stringify(justification)}
        ) {
          success
        }
      }`;

      new Xhr().request(gQry, "An error occurred requesting verification")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          if (data.requestVerification.success) {
            dispatch<IActionStructure>(closeRemediationMdl());
            msgSuccess(
              translate.t("proj_alerts.verified_success"),
              translate.t("proj_alerts.updated_title"),
            );
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred verifying finding");
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

