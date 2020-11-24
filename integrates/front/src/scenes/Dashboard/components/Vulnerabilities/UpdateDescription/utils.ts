import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import type { IVulnDataType } from "scenes/Dashboard/components/Vulnerabilities/types";
import _ from "lodash";

const emptyTreatment: IHistoricTreatment = {
  acceptanceDate: "",
  acceptanceStatus: "",
  date: "",
  justification: "",
  treatment: "",
  treatmentManager: "",
  user: "",
};

const sortTags: (tags: string) => string[] = (tags: string): string[] => {
  const tagSplit: string[] = tags.trim().split(",");

  return tagSplit.map((tag: string): string => tag.trim());
};

const groupExternalBts: (vulnerabilities: IVulnDataType[]) => string = (
  vulnerabilities: IVulnDataType[]
): string => {
  const bts: string = vulnerabilities.reduce(
    (acc: string, vuln: IVulnDataType): string =>
      _.isEmpty(vuln.externalBts) ? acc : vuln.externalBts,
    ""
  );

  return vulnerabilities.every((row: IVulnDataType): boolean =>
    _.isEmpty(row.externalBts) ? true : row.externalBts === bts
  )
    ? bts
    : "";
};

const getLastTreatment: (
  historic: IHistoricTreatment[]
) => IHistoricTreatment = (
  historic: IHistoricTreatment[]
): IHistoricTreatment => {
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

const groupLastHistoricTreatment: (
  vulnerabilities: IVulnDataType[]
) => IHistoricTreatment = (
  vulnerabilities: IVulnDataType[]
): IHistoricTreatment => {
  const attributeToOmitWhenComparing: string[] = ["date", "user"];
  const treatment: IHistoricTreatment = vulnerabilities.reduce(
    (acc: IHistoricTreatment, vuln: IVulnDataType): IHistoricTreatment => {
      const lastTreatment: IHistoricTreatment = getLastTreatment(
        vuln.historicTreatment
      );

      return !_.some(lastTreatment, _.isEmpty) ? acc : lastTreatment;
    },
    emptyTreatment
  );

  return vulnerabilities.every((vuln: IVulnDataType): boolean => {
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

export {
  getLastTreatment,
  groupExternalBts,
  groupLastHistoricTreatment,
  sortTags,
};
