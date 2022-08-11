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

export { filterByState, filterByTreatment };
