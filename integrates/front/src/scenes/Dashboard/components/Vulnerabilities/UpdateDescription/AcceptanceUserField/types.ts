import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IAcceptanceUserFieldProps {
  isAcceptedSelected: boolean;
  isAcceptedUndefinedSelected: boolean;
  isInProgressSelected: boolean;
  lastTreatment: IHistoricTreatment;
}

export { IAcceptanceUserFieldProps };
