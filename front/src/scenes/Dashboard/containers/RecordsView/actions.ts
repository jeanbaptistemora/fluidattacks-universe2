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

export const loadRecords: ((findingId: string) => ThunkResult<void>) = (findingId: string): ThunkResult<void> =>
  (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `{
    finding(identifier: "${findingId}") {
      records
    }
  }`;
    new Xhr().request(gQry, "An error occurred getting compromised records")
      .then((response: AxiosResponse) => {
        const { data } = response.data;
        dispatch({
          payload: { records: JSON.parse(data.finding.records) },
          type: actionTypes.LOAD_RECORDS,
        });
      })
      .catch((error: AxiosError) => {
        if (error.response !== undefined) {
          const { errors } = error.response.data;

          msgError("There was an error :(");
          rollbar.error(error.message, errors);
        }
      });
  };

export const editRecords: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.EDIT_RECORDS,
  });

export const removeRecords: ((findingId: string) => ThunkResult<void>) = (findingId: string): ThunkResult<void> =>
  (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      removeEvidence (
        evidenceId: "8",
        findingId: "${findingId}") {
        success
        finding {
          records
        }
      }
    }`;
    new Xhr().request(gQry, "An error occurred removing records")
      .then((response: AxiosResponse) => {
        const { data } = response.data;
        if (data.removeEvidence.success) {
          msgSuccess(
            translate.t("proj_alerts.records_removed"),
            translate.t("search_findings.tab_users.title_success"),
          );
          location.reload();
        } else {
          msgError(translate.t("proj_alerts.error_textsad"));
        }
      })
      .catch((error: AxiosError) => {
        if (error.response !== undefined) {
          const { errors } = error.response.data;
          msgError(errors[0].message);
        }
      });
  };

export const updateRecords: ((findingId: string) => ThunkResult<void>) = (findingId: string): ThunkResult<void> =>
  (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
    updateEvidence (
      evidenceId: "8",
      findingId: "${findingId}", file: "") {
      success
      finding {
        records
      }
    }
  }`;
    new Xhr().upload(gQry, "#evidence8", "An error occurred updating records")
      .then((response: AxiosResponse) => {
        const { data } = response.data;
        if (data.updateEvidence.success) {
          msgSuccess(
            translate.t("proj_alerts.file_updated"),
            translate.t("search_findings.tab_users.title_success"),
          );
          location.reload();
        } else {
          msgError(translate.t("proj_alerts.error_textsad"));
        }
      })
      .catch((error: AxiosError) => {
        if (error.response !== undefined) {
          const { errors } = error.response.data;

          switch (errors[0].message) {
            case "Exception - Invalid File Size":
              msgError(translate.t("proj_alerts.file_size"));
              break;
            case "Exception - Invalid File Type":
              msgError(translate.t("proj_alerts.file_type_wrong"));
              break;
            case "Wrong file structure":
              msgError(translate.t("proj_alerts.invalid_structure"));
              break;
            default:
              msgError(translate.t("proj_alerts.no_file_update"));
              rollbar.error(error.message, errors);
          }

        }
      });
  };
