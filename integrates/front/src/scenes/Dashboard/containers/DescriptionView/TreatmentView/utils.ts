import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { formatHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/utils";

export const getPreviousTreatment: (
  historic: IHistoricTreatment[]
) => IHistoricTreatment[] = (
  historic: IHistoricTreatment[]
): IHistoricTreatment[] => {
  const previousTreatment: IHistoricTreatment[] = [...historic];
  // Reverse is actually mutating a copy created by the spread operator.
  // eslint-disable-next-line fp/no-mutating-methods
  previousTreatment.reverse();

  return previousTreatment.map(
    (treatment: IHistoricTreatment): IHistoricTreatment =>
      formatHistoricTreatment(treatment, true)
  );
};
