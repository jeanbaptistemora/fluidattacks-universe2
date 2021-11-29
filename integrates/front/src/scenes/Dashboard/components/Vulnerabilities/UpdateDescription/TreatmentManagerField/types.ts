import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface ITreatmentManagerFieldProps {
  isAcceptedSelected: boolean;
  isAcceptedUndefinedSelected: boolean;
  isInProgressSelected: boolean;
  lastTreatment: IHistoricTreatment;
  userEmails: string[];
}

export { ITreatmentManagerFieldProps };
