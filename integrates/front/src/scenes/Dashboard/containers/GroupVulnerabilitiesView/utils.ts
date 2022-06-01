import type { IVulnerability } from "./types";

import { linkFormatter } from "components/Table/formatters";

const filterByState = (
  state: string
): ((vulnerability: IVulnerability) => boolean) => {
  return (vulnerability: IVulnerability): boolean => {
    return vulnerability.currentState === state;
  };
};

const filterByTreatment = (
  treatment: string
): ((vulnerability: IVulnerability) => boolean) => {
  return (vulnerability: IVulnerability): boolean => {
    return vulnerability.treatment === treatment;
  };
};

const formatEvidence = (
  _cell: string,
  row: IVulnerability,
  rowIndex: number
): React.ReactNode => {
  return linkFormatter<IVulnerability>(
    (): string => `${row.finding.id}/evidence`
  )("View", row, rowIndex);
};

const formatLocation = (
  _cell: string,
  row: IVulnerability
): React.ReactNode => {
  return `${row.where} | ${row.specific}`;
};

export { filterByState, filterByTreatment, formatEvidence, formatLocation };
