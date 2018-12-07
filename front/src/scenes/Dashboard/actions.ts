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
import { ISeverityViewProps } from "./components/SeverityView";

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

export const editSeverity: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.EDIT_SEVERITY,
  });

export const calcCVSSv2: DashboardAction =
  (data: ISeverityViewProps["dataset"]): IActionStructure => {
    let BASESCORE_FACTOR_1: number; BASESCORE_FACTOR_1 = 0.6;
    let BASESCORE_FACTOR_2: number; BASESCORE_FACTOR_2 = 0.4;
    let BASESCORE_FACTOR_3: number; BASESCORE_FACTOR_3 = 1.5;
    let IMPACT_FACTOR: number; IMPACT_FACTOR = 10.41;
    let EXPLOITABILITY_FACTOR: number; EXPLOITABILITY_FACTOR = 20;
    let F_IMPACT_FACTOR: number; F_IMPACT_FACTOR = 1.176;

    const impCon: number = parseFloat(data.confidentialityImpact);
    const impInt: number = parseFloat(data.integrityImpact);
    const impDis: number = parseFloat(data.availabilityImpact);
    const accCom: number = parseFloat(data.accessComplexity);
    const accVec: number = parseFloat(data.accessVector);
    const auth: number = parseFloat(data.authentication);
    const explo: number = parseFloat(data.exploitability);
    const resol: number = parseFloat(data.resolutionLevel);
    const confi: number = parseFloat(data.confidenceLevel);

    /*
     * The constants above are part of the BaseScore, Impact and
     * Exploibility equations
     * More information in https://www.first.org/cvss/v2/guide
     */
    const impact: number = IMPACT_FACTOR * (1 - ((1 - impCon) * (1 - impInt) * (1 - impDis)));
    const exploitabilty: number = EXPLOITABILITY_FACTOR * accCom * auth * accVec;
    const baseScore: number = ((BASESCORE_FACTOR_1 * impact) + (BASESCORE_FACTOR_2 * exploitabilty)
                              - BASESCORE_FACTOR_3) * F_IMPACT_FACTOR;
    const temporal: number = baseScore * explo * resol * confi;

    return ({
      payload: {
        baseScore: baseScore.toFixed(1),
        temporal: temporal.toFixed(1),
      },
      type: actionType.CALC_CVSSV2,
    });
  };

export const loadSeverity: ThunkActionStructure =
  (findingId: string): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `{
      finding(identifier: "${findingId}") {
        severity
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting severity")
    .then((response: AxiosResponse) => {
      const { data } = response.data;
      dispatch(calcCVSSv2(data.finding.severity));
      dispatch({
        payload: {
          dataset: data.finding.severity,
        },
        type: actionType.LOAD_SEVERITY,
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

export const openConfirmMdl: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.OPEN_CONFIRM_MDL,
});

export const closeConfirmMdl: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.CLOSE_CONFIRM_MDL,
});

export const updateSeverity: ThunkActionStructure =
  (findingId: string, values: ISeverityViewProps["dataset"],
   criticity: ISeverityViewProps["criticity"]): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      updateSeverity(
        findingId: "${findingId}",
        data: {
          accessComplexity: "${values.accessComplexity}",
          accessVector: "${values.accessVector}",
          authentication: "${values.authentication}",
          availabilityImpact: "${values.availabilityImpact}",
          confidenceLevel: "${values.confidenceLevel}",
          confidentialityImpact: "${values.confidentialityImpact}",
          criticity: "${criticity}",
          exploitability: "${values.exploitability}",
          id: "${findingId}",
          integrityImpact: "${values.integrityImpact}",
          resolutionLevel: "${values.resolutionLevel}",
          collateralDamagePotential: "${values.collateralDamagePotential}",
          findingDistribution: "${values.findingDistribution}",
          confidentialityRequirement: "${values.confidentialityRequirement}",
          integrityRequirement: "${values.integrityRequirement}",
          availabilityRequirement: "${values.availabilityRequirement}",
        }
      ) {
        success
        finding {
          severity
        }
      }
    }`;
    new Xhr().request(gQry, "An error occurred updating severity")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      if (data.updateSeverity.success) {
        dispatch(calcCVSSv2(data.updateSeverity.finding.severity));
        dispatch({
          payload: {
            dataset: data.updateSeverity.finding.severity,
          },
          type: actionType.LOAD_SEVERITY,
        });
        dispatch(editSeverity());
        dispatch(closeConfirmMdl());
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
