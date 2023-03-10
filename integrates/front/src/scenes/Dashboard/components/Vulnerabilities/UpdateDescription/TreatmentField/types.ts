import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";

interface ITreatmentFieldProps {
  areSelectedSubmittedVulnerabilities: boolean;
  isTreatmentPristine: boolean;
  lastTreatment: IHistoricTreatment;
}

export type { ITreatmentFieldProps };
