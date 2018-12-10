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

type DashboardAction = ((...args: any[]) => IActionStructure);
type ThunkDispatcher = Dispatch<Action> & ThunkDispatch<{}, {}, AnyAction>;
type ThunkActionStructure = ((...args: any[]) => ThunkAction<void, {}, {}, AnyAction>);

export const addFileName: DashboardAction =
  (newValue: string): IActionStructure => ({
      payload: {
        newValue,
      },
      type: actionType.ADD_FILE_NAME,
});

export const loadVulnerabilities: ThunkActionStructure =
  (findingId: string): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `{
      finding(identifier: "${findingId}") {
        id
        success
        errorMessage
        portsVulns: vulnerabilities(
          vulnType: "ports") {
          ...vulnInfo
        }
        linesVulns: vulnerabilities(
          vulnType: "lines") {
          ...vulnInfo
        }
        inputsVulns: vulnerabilities(
          vulnType: "inputs") {
          ...vulnInfo
        }
      }
    }
    fragment vulnInfo on Vulnerability {
      vulnType
      where
      specific
      currentState
      id
      findingId
    }`;
    new Xhr().request(gQry, "An error occurred getting vulnerabilities")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      if (data.finding.success) {
        dispatch({
          payload: {
            dataInputs: data.finding.inputsVulns,
            dataLines: data.finding.linesVulns,
            dataPorts: data.finding.portsVulns,
          },
          type: actionType.LOAD_VULNERABILITIES,
        });
      } else if (data.finding.errorMessage === "Error in file") {
        msgError(translate.t("search_findings.tab_description.errorFileVuln"));
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

export const deleteVulnerability: ThunkActionStructure =
  (vulnInfo: { [key: string]: string }): ThunkAction<void, {}, {}, Action> =>
    (_: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      deleteVulnerability(id: "${vulnInfo.id}", findingId: "${vulnInfo.findingId}"){
        success
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting vulnerabilities")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      if (data.deleteVulnerability.success) {
        msgSuccess(
          translate.t("search_findings.tab_description.vulnDeleted"),
          translate.t("proj_alerts.title_success"));
        location.reload();
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

export const loadExploit: ThunkActionStructure =
  (findingId: string): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `{
      finding(identifier: "${findingId}") {
        exploit
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting exploit")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      dispatch({
        payload: {
          code: data.finding.exploit,
        },
        type: actionType.LOAD_EXPLOIT,
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

export const editExploit: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.EDIT_EXPLOIT,
  });

export const updateExploit: ThunkActionStructure =
  (
    findingId: string, projectName: string,
  ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
  let gQry: string;
  gQry = `mutation {
    updateEvidence (
      id: "7",
      findingId: "${findingId}",
      projectName: "${projectName}") {
      success
      finding {
        exploit
      }
    }
  }`;
  new Xhr().upload(gQry, "#evidence7", "An error occurred updating exploit")
  .then((response: AxiosResponse) => {
    const { data } = response.data;
    if (data.updateEvidence.success) {
      dispatch({
        payload: { code: data.updateEvidence.finding.exploit },
        type: actionType.LOAD_EXPLOIT,
      });
      msgSuccess(
        translate.t("proj_alerts.file_updated"),
        translate.t("search_findings.tab_users.title_success"),
      );
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

export const openEvidence: DashboardAction =
  (imgIndex: number): IActionStructure => ({
    payload: { imgIndex },
    type: actionType.OPEN_EVIDENCE,
  });

export const closeEvidence: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.CLOSE_EVIDENCE,
  });

export const moveEvidenceIndex: DashboardAction =
  (currentIndex: number, totalImages: number, direction: "next" | "previous"): IActionStructure => ({
    payload: {
      index: (direction === "next" ? (currentIndex + 1) : (currentIndex + totalImages - 1))
        % totalImages,
    },
    type: actionType.MOVE_EVIDENCE,
  });
