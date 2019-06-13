/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */
import { AxiosError, AxiosResponse } from "axios";
import { Action, AnyAction, Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError, msgSuccess } from "../../utils/notifications";
import rollbar from "../../utils/rollbar";
import translate from "../../utils/translations/translate";
import Xhr from "../../utils/xhr";
import * as actionType from "./actionTypes";

export interface IActionStructure {
  payload: any;
  type: string;
}

export type ThunkDispatcher = Dispatch<Action> & ThunkDispatch<{}, {}, AnyAction>;
type ThunkActionStructure = ((...args: any[]) => ThunkAction<void, {}, {}, AnyAction>);

export const updateVulnerabilities: ThunkActionStructure =
  (findingId: string): ThunkAction<void, {}, {}, Action> => (_: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      uploadFile(findingId: "${findingId}") {
        success
      }
    }`;
    new Xhr().upload(gQry, "#vulnerabilities", "An error occurred updating vulnerabilities")
      .then((response: AxiosResponse) => {
        const { data } = response.data;

        if (data.uploadFile.success) {
          msgSuccess(
            translate.t("proj_alerts.file_updated"),
            translate.t("proj_alerts.title_success"));
          location.reload();
        } else {
          msgError(translate.t("proj_alerts.error_textsad"));
        }
      })
      .catch((error: AxiosError) => {
        if (error.response !== undefined) {
          const { errors } = error.response.data;

          switch (errors[0].message) {
            case "Exception - Error in range limit numbers":
              msgError(translate.t("proj_alerts.range_error"));
              break;
            case "Exception - Invalid Schema":
              msgError(translate.t("proj_alerts.invalid_schema"));
              break;
            case "Exception - Invalid File Size":
              msgError(translate.t("proj_alerts.file_size_py"));
              break;
            case "Exception - Invalid File Type":
              msgError(translate.t("proj_alerts.file_type_yaml"));
              break;
            case "Exception - Error in port value":
              msgError(translate.t("proj_alerts.port_value"));
              break;
            case "Exception - Error in specific value":
              msgError(translate.t("proj_alerts.port_value"));
              break;
            default:
              msgError(translate.t("proj_alerts.invalid_specific"));
              rollbar.error(error.message, errors);
          }
        }
      });
  };

export const openConfirmDialog: ((dialogName: string) => IActionStructure) =
  (dialogName: string): IActionStructure => ({
    payload: { dialogName },
    type: actionType.OPEN_CONFIRM_DIALOG,
  });

export const closeConfirmDialog: ((dialogName: string) => IActionStructure) =
  (dialogName: string): IActionStructure => ({
    payload: { dialogName },
    type: actionType.CLOSE_CONFIRM_DIALOG,
  });
