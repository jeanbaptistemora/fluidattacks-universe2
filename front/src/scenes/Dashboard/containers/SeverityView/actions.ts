import { AxiosError, AxiosResponse } from "axios";
import { Action, AnyAction, Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import * as actionTypes from "./actionTypes";
import { ISeverityViewProps } from "./index";

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

export const editSeverity: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.EDIT_SEVERITY,
  });

export const calcCVSSv2: ((data: ISeverityViewProps["dataset"]) => number) =
  (data: ISeverityViewProps["dataset"]): number => {
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
    F_IMPACT_FACTOR = impact === 0 ? 0 : 1.176;
    const exploitabilty: number = EXPLOITABILITY_FACTOR * accCom * auth * accVec;
    const baseScore: number = ((BASESCORE_FACTOR_1 * impact) + (BASESCORE_FACTOR_2 * exploitabilty)
      - BASESCORE_FACTOR_3) * F_IMPACT_FACTOR;
    const temporal: number = baseScore * explo * resol * confi;

    return temporal;
  };

export const calcPrivilegesRequired: ((privileges: string, scope: string) => number) =
  (privileges: string, scope: string): number => {
    let privReq: number = parseFloat(privileges);
    if (parseFloat(scope) === 1) {
      if (privReq === 0.62) {
        privReq = 0.68;
      } else if (privReq === 0.27) {
        privReq = 0.5;
      }
    } else {
      if (privReq === 0.68) {
        privReq = 0.62;
      } else if (privReq === 0.5) {
        privReq = 0.27;
      }
    }

    return privReq;
  };

export const calcCVSSv3: ((data: ISeverityViewProps["dataset"]) => number) =
  (data: ISeverityViewProps["dataset"]): number => {
    let BASESCORE_FACTOR: number; BASESCORE_FACTOR = 1.08;
    let IMPACT_FACTOR_1: number; IMPACT_FACTOR_1 = 6.42;
    let IMPACT_FACTOR_2: number; IMPACT_FACTOR_2 = 7.52;
    let IMPACT_FACTOR_3: number; IMPACT_FACTOR_3 = 0.029;
    let IMPACT_FACTOR_4: number; IMPACT_FACTOR_4 = 3.25;
    let IMPACT_FACTOR_5: number; IMPACT_FACTOR_5 = 0.02;
    let IMPACT_FACTOR_6: number; IMPACT_FACTOR_6 = 15;
    let EXPLOITABILITY_FACTOR_1: number; EXPLOITABILITY_FACTOR_1 = 8.22;

    const impCon: number = parseFloat(data.confidentialityImpact);
    const impInt: number = parseFloat(data.integrityImpact);
    const impDis: number = parseFloat(data.availabilityImpact);
    const sevScope: number = parseFloat(data.severityScope);
    const attVec: number = parseFloat(data.attackVector);
    const attCom: number = parseFloat(data.attackComplexity);
    const privReq: number = calcPrivilegesRequired(data.privilegesRequired, data.severityScope);
    const usrInt: number = parseFloat(data.userInteraction);
    const explo: number = parseFloat(data.exploitability);
    const remLev: number = parseFloat(data.remediationLevel);
    const repConf: number = parseFloat(data.reportConfidence);

    const iscBase: number = 1 - ((1 - impCon) * (1 - impInt) * (1 - impDis));

    const impact: number = (sevScope === 1)
      ? ((IMPACT_FACTOR_2 * (iscBase - IMPACT_FACTOR_3)) -
        (IMPACT_FACTOR_4 * Math.pow((iscBase - IMPACT_FACTOR_5), IMPACT_FACTOR_6)))
      : IMPACT_FACTOR_1 * iscBase;
    const exploitability: number = (EXPLOITABILITY_FACTOR_1 * attVec * attCom * privReq * usrInt);

    const basescore: number = (impact <= 0)
      ? 0
      : ((sevScope === 1)
          ? Math.ceil(Math.min(BASESCORE_FACTOR * (impact + exploitability), 10) * 10) / 10
          : Math.ceil(Math.min(impact + exploitability, 10) * 10) / 10);

    const temporal: number = Math.ceil(basescore * explo * remLev * repConf * 10) / 10;

    return temporal;
  };

export const calcCVSS:
((data: ISeverityViewProps["dataset"], cvssVersion: ISeverityViewProps["cvssVersion"]) => IActionStructure) =
  (data: ISeverityViewProps["dataset"], cvssVersion: ISeverityViewProps["cvssVersion"]): IActionStructure => {
    const temporal: number = (cvssVersion === "3")
    ? calcCVSSv3(data)
    : calcCVSSv2(data);

    return ({
    payload: {
      temporal: temporal.toFixed(1),
    },
    type: actionTypes.CALC_CVSS,
  });
};

export const loadSeverity: ThunkActionStructure =
  (findingId: string): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `{
      finding(identifier: "${findingId}") {
        cvssVersion
        severity
      }
    }`;
      new Xhr().request(gQry, "An error occurred getting severity")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          dispatch(calcCVSS(data.finding.severity, data.finding.cvssVersion));
          dispatch({
            payload: {
              cvssVersion: data.finding.cvssVersion,
              dataset: data.finding.severity,
            },
            type: actionTypes.LOAD_SEVERITY,
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

export const updateSeverity: ThunkActionStructure =
  (findingId: string, values: ISeverityViewProps["dataset"] & { cvssVersion: string },
   criticity: ISeverityViewProps["criticity"]): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `mutation {
      updateSeverity(
        findingId: "${findingId}",
        data: {
          accessComplexity: "${values.accessComplexity}",
          accessVector: "${values.accessVector}",
          attackComplexity: "${values.attackComplexity}",
          attackVector: "${values.attackVector}",
          authentication: "${values.authentication}",
          availabilityImpact: "${values.availabilityImpact}",
          availabilityRequirement: "${values.availabilityRequirement}",
          collateralDamagePotential: "${values.collateralDamagePotential}",
          confidenceLevel: "${values.confidenceLevel}",
          confidentialityImpact: "${values.confidentialityImpact}",
          confidentialityRequirement: "${values.confidentialityRequirement}",
          criticity: "${criticity}",
          cvssVersion: "${values.cvssVersion}",
          exploitability: "${values.exploitability}",
          findingDistribution: "${values.findingDistribution}",
          id: "${findingId}",
          integrityImpact: "${values.integrityImpact}",
          integrityRequirement: "${values.integrityRequirement}",
          modifiedAttackComplexity: "${values.modifiedAttackComplexity}",
          modifiedAttackVector: "${values.modifiedAttackVector}",
          modifiedAvailabilityImpact: "${values.modifiedAvailabilityImpact}",
          modifiedConfidentialityImpact: "${values.modifiedConfidentialityImpact}",
          modifiedIntegrityImpact: "${values.modifiedIntegrityImpact}",
          modifiedPrivilegesRequired: "${values.modifiedPrivilegesRequired}",
          modifiedSeverityScope: "${values.modifiedSeverityScope}",
          modifiedUserInteraction: "${values.modifiedUserInteraction}",
          privilegesRequired: "${values.privilegesRequired}",
          remediationLevel: "${values.remediationLevel}",
          reportConfidence: "${values.reportConfidence}",
          severityScope: "${values.severityScope}",
          resolutionLevel: "${values.resolutionLevel}",
          userInteraction: "${values.userInteraction}",
        }
      ) {
        success
        finding {
          cvssVersion
          severity
        }
      }
    }`;
      new Xhr().request(gQry, "An error occurred updating severity")
        .then((response: AxiosResponse) => {
          const { data } = response.data;

          if (data.updateSeverity.success) {
            dispatch(calcCVSS(data.updateSeverity.finding.severity, data.updateSeverity.finding.cvssVersion));
            dispatch({
              payload: {
                cvssVersion: data.updateSeverity.finding.cvssVersion,
                dataset: data.updateSeverity.finding.severity,
              },
              type: actionTypes.LOAD_SEVERITY,
            });
            dispatch(editSeverity());
            msgSuccess(
              translate.t("proj_alerts.updated"),
              translate.t("proj_alerts.updated_title"),
            );
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
