import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";

interface IAssignedFieldProps {
  isAcceptedSelected: boolean;
  isAcceptedUndefinedSelected: boolean;
  isInProgressSelected: boolean;
  lastTreatment: IHistoricTreatment;
  userEmails: string[];
}

export type { IAssignedFieldProps };
