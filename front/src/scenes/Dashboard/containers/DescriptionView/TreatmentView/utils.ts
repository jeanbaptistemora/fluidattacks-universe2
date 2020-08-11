import { IHistoricTreatment } from "../types";
import { formatHistoricTreatment } from "../utils";

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
