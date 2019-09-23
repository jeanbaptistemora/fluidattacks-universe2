/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */
import { AxiosError, AxiosResponse } from "axios";
import { Action, AnyAction, Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError, msgErrorStick, msgSuccess } from "../../utils/notifications";
import rollbar from "../../utils/rollbar";
import translate from "../../utils/translations/translate";
import Xhr from "../../utils/xhr";
import * as actionType from "./actionTypes";

export interface IActionStructure {
  payload?: any;
  type: string;
}

export type ThunkDispatcher = Dispatch<Action> & ThunkDispatch<{}, {}, AnyAction>;
type ThunkActionStructure = ((...args: any[]) => ThunkAction<void, {}, {}, AnyAction>);

const formatError: (errorName: string, errorValue: string) => string =
  (errorName: string, errorValue: string): string =>
    (` ${translate.t(errorName)} "${errorValue}" ${translate.t("proj_alerts.invalid")}. `);

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

          if (errors[0].message.includes("Exception - Error in range limit numbers")) {
            const errorObject: any = JSON.parse(errors[0].message);
            msgError(`${translate.t("proj_alerts.range_error")} ${errorObject.values}`);
          } else if (errors[0].message.includes("Exception - Invalid Schema")) {
            const errorObject: any = JSON.parse(errors[0].message);
            if (errorObject.values.length > 0 || errorObject.keys.length > 0) {
              const listValuesFormated: string[] = errorObject.values.map(
                (x: string) => formatError("proj_alerts.value", x));
              const listKeysFormated: string[] = errorObject.keys.map(
                (x: string) => formatError("proj_alerts.key", x));
              msgErrorStick(
                listKeysFormated.join("") + listValuesFormated.join(""),
                translate.t("proj_alerts.invalid_schema"));
            } else {
              msgError(translate.t("proj_alerts.invalid_schema"));
            }
          } else if (errors[0].message === "Exception - Invalid File Size") {
            msgError(translate.t("proj_alerts.file_size_py"));
          } else if (errors[0].message === "Exception - Invalid File Type") {
            msgError(translate.t("proj_alerts.file_type_yaml"));
          } else if (errors[0].message.includes("Exception - Error in path value")) {
            const errorObject: any = JSON.parse(errors[0].message);
            msgErrorStick(`${translate.t("proj_alerts.path_value")}
              ${formatError("proj_alerts.value", errorObject.values)}`);
          } else if (errors[0].message.includes("Exception - Error in port value")) {
            const errorObject: any = JSON.parse(errors[0].message);
            msgErrorStick(`${translate.t("proj_alerts.port_value")}
              ${formatError("proj_alerts.value", errorObject.values)}`);
          } else if (errors[0].message === "Exception - Error in specific value") {
            msgError(translate.t("proj_alerts.invalid_specific"));
          } else {
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

export const openUpdateAccessToken: (() => IActionStructure) =
  (): IActionStructure => ({
    type: actionType.OPEN_ACCESS_TOKEN_MODAL,
  });

export const closeUpdateAccessToken: (() => IActionStructure) =
  (): IActionStructure => ({
    type: actionType.CLOSE_ACCESS_TOKEN_MODAL,
  });
