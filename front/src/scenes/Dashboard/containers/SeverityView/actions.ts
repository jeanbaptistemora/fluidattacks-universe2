import { AxiosError, AxiosResponse } from "axios";
import { Action, AnyAction, Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError } from "../../../../utils/notifications";
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

export const calcCVSSv2: ((data: ISeverityViewProps["dataset"]) => IActionStructure) =
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
    if (impact === 0){
      F_IMPACT_FACTOR = 0;
    } else {
      F_IMPACT_FACTOR = 1.176;
    };
    const exploitabilty: number = EXPLOITABILITY_FACTOR * accCom * auth * accVec;
    const baseScore: number = ((BASESCORE_FACTOR_1 * impact) + (BASESCORE_FACTOR_2 * exploitabilty)
      - BASESCORE_FACTOR_3) * F_IMPACT_FACTOR;
    const temporal: number = baseScore * explo * resol * confi;

    return ({
      payload: {
        temporal: temporal.toFixed(1),
      },
      type: actionTypes.CALC_CVSSV2,
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
              type: actionTypes.LOAD_SEVERITY,
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
