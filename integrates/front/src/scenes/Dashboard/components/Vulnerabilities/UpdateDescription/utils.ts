import _ from "lodash";

import type { IVulnDataTypeAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

const emptyTreatment: IHistoricTreatment = {
  acceptanceDate: "",
  acceptanceStatus: "",
  assigned: "",
  date: "",
  justification: "",
  treatment: "",
  user: "",
};

const sortTags: (tags: string) => string[] = (tags: string): string[] => {
  const tagSplit: string[] = tags.trim().split(",");

  return tagSplit.map((tag: string): string => tag.trim());
};

const groupExternalBugTrackingSystem: (
  vulnerabilities: IVulnDataTypeAttr[]
) => string = (vulnerabilities: IVulnDataTypeAttr[]): string => {
  const bts: string = vulnerabilities.reduce(
    (acc: string, vuln: IVulnDataTypeAttr): string =>
      _.isEmpty(vuln.externalBugTrackingSystem) ||
      vuln.externalBugTrackingSystem === undefined
        ? acc
        : vuln.externalBugTrackingSystem,
    ""
  );

  return vulnerabilities.every((row: IVulnDataTypeAttr): boolean =>
    _.isEmpty(row.externalBugTrackingSystem)
      ? true
      : row.externalBugTrackingSystem === bts
  )
    ? bts
    : "";
};

const getLastTreatment: (historic: IHistoricTreatment[]) => IHistoricTreatment =
  (historic: IHistoricTreatment[]): IHistoricTreatment => {
    const lastTreatment: IHistoricTreatment =
      historic.length > 0
        ? (_.last(historic) as IHistoricTreatment)
        : emptyTreatment;

    return {
      ...lastTreatment,
      acceptanceDate: _.isNull(lastTreatment.acceptanceDate)
        ? ""
        : _.get(lastTreatment, "acceptanceDate", "").split(" ")[0],
      treatment: lastTreatment.treatment.replace(" ", "_"),
    };
  };

const hasNewTreatment: (vulns: IVulnDataTypeAttr[]) => boolean = (
  vulns: IVulnDataTypeAttr[]
): boolean => {
  return (
    vulns.filter((vuln): boolean => {
      const lastTreatment: IHistoricTreatment = getLastTreatment(
        vuln.historicTreatment
      );

      return lastTreatment.treatment === "NEW";
    }).length > 0
  );
};

const groupLastHistoricTreatment: (
  vulnerabilities: IVulnDataTypeAttr[]
) => IHistoricTreatment = (
  vulnerabilities: IVulnDataTypeAttr[]
): IHistoricTreatment => {
  const attributeToOmitWhenComparing: string[] = ["date", "user"];
  const treatment: IHistoricTreatment = vulnerabilities.reduce(
    (acc: IHistoricTreatment, vuln: IVulnDataTypeAttr): IHistoricTreatment => {
      const lastTreatment: IHistoricTreatment = getLastTreatment(
        vuln.historicTreatment
      );

      return _.some(lastTreatment, _.isEmpty) ? lastTreatment : acc;
    },
    emptyTreatment
  );

  return vulnerabilities.every((vuln: IVulnDataTypeAttr): boolean => {
    const lastTreatment: IHistoricTreatment = getLastTreatment(
      vuln.historicTreatment
    );

    return _.some(lastTreatment, _.isEmpty)
      ? _.isEqual(
          _.omit(lastTreatment, attributeToOmitWhenComparing),
          _.omit(treatment, attributeToOmitWhenComparing)
        )
      : true;
  })
    ? treatment
    : emptyTreatment;
};

const groupVulnLevel: (vulnerabilities: IVulnDataTypeAttr[]) => string = (
  vulnerabilities: IVulnDataTypeAttr[]
): string => {
  const vulnLevel: string = vulnerabilities.reduce(
    (acc: string, vuln: IVulnDataTypeAttr): string =>
      _.isEmpty(vuln.severity) ? acc : vuln.severity,
    ""
  );

  return vulnerabilities.every((row: IVulnDataTypeAttr): boolean =>
    _.isEmpty(row.severity) ? true : row.severity === vulnLevel
  )
    ? vulnLevel
    : "";
};

export {
  getLastTreatment,
  groupExternalBugTrackingSystem,
  groupLastHistoricTreatment,
  groupVulnLevel,
  sortTags,
  hasNewTreatment,
};
