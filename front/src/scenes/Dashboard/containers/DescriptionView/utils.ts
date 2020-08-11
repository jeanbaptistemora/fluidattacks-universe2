import { IHistoricTreatment } from "./types";
import _ from "lodash";
import { formatTreatment } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";

export const formatCweUrl: (cweId: string) => string = (
  cweId: string
): string =>
  _.includes(["None", ""], cweId)
    ? "-"
    : `https://cwe.mitre.org/data/definitions/${cweId}.html`;

export const formatFindingType: (type: string) => string = (
  type: string
): string =>
  _.isEmpty(type)
    ? "-"
    : translate.t(`search_findings.tab_description.type.${type.toLowerCase()}`);

export const formatCompromisedRecords: (records: number) => string = (
  records: number
): string => records.toString();

export const formatHistoricTreatment: (
  treatmentEvent: IHistoricTreatment,
  translateTreatment: boolean
) => IHistoricTreatment = (
  treatmentEvent: IHistoricTreatment,
  translateTreatment: boolean
): IHistoricTreatment => {
  const date: string = _.get(treatmentEvent, "date", "").split(" ")[0];
  const acceptanceDate: string = (_.get(
    treatmentEvent,
    "acceptance_date",
    ""
  ) as string).split(" ")[0];
  const acceptanceStatus: string = (_.get(
    treatmentEvent,
    "acceptance_status",
    ""
  ) as string).split(" ")[0];
  const treatment: string = translateTreatment
    ? formatTreatment(
        _.get(treatmentEvent, "treatment").replace(" ", "_"),
        "open"
      )
    : _.get(treatmentEvent, "treatment").replace(" ", "_");
  const justification: string = _.get(treatmentEvent, "justification", "");
  const acceptationUser: string = _.get(treatmentEvent, "user", "");

  return {
    acceptanceDate,
    acceptanceStatus,
    date,
    justification,
    treatment,
    user: acceptationUser,
  };
};

export const getLastTreatment: (
  historic: IHistoricTreatment[]
) => IHistoricTreatment = (
  historic: IHistoricTreatment[]
): IHistoricTreatment => {
  const lastTreatment: IHistoricTreatment =
    historic.length > 0
      ? (_.last(historic) as IHistoricTreatment)
      : { date: "", treatment: "", user: "" };

  return formatHistoricTreatment(lastTreatment, false);
};
