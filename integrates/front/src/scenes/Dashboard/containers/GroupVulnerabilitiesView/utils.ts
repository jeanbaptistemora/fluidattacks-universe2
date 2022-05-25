import type { IVulnerability } from "./types";

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

const formatLocation = (
  _cell: string,
  row: IVulnerability
): React.ReactNode => {
  return `${row.where} | ${row.specific}`;
};

export { filterByState, filterByTreatment, formatLocation };
