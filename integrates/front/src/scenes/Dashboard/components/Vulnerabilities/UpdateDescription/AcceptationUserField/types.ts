import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IAcceptationUserFieldProps {
  isAcceptedSelected: boolean;
  isAcceptedUndefinedSelected: boolean;
  isInProgressSelected: boolean;
  lastTreatment: IHistoricTreatment;
}

export { IAcceptationUserFieldProps };
