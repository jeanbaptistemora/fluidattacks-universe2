import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface ITreatmentManagerFieldProps {
  isInProgressSelected: boolean;
  lastTreatment: IHistoricTreatment;
  userEmails: string[];
}

export { ITreatmentManagerFieldProps };
