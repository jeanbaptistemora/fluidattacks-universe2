import { createContext } from "react";

import type {
  IUpdateTreatmentVulnerabilityForm,
  IVulnerabilityModalValues,
} from "./types";

const defaultValue: IUpdateTreatmentVulnerabilityForm = {
  acceptanceDate: undefined,
  externalBts: "",
  justification: undefined,
  severity: undefined,
  tag: "",
  treatment: "",
  treatmentManager: undefined,
};

const UpdateDescriptionContext = createContext<IVulnerabilityModalValues>([
  defaultValue,
  (): void => undefined,
]);

export { defaultValue, UpdateDescriptionContext };
