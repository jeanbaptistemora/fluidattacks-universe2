import { ISeverityAttr } from "../scenes/Dashboard/containers/SeverityView/types";

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

export const calcCVSSv3: ((data: ISeverityAttr["finding"]["severity"]) => number) =
  (data: ISeverityAttr["finding"]["severity"]): number => {
    const BASESCORE_FACTOR: number = 1.08;
    const IMPACT_FACTOR_1: number = 6.42;
    const IMPACT_FACTOR_2: number = 7.52;
    const IMPACT_FACTOR_3: number = 0.029;
    const IMPACT_FACTOR_4: number = 3.25;
    const IMPACT_FACTOR_5: number = 0.02;
    const IMPACT_FACTOR_6: number = 15;
    const EXPLOITABILITY_FACTOR_1: number = 8.22;

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

    return isNaN(temporal) ? 0 : temporal;
  };
