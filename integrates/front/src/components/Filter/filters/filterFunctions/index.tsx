import type { Dispatch, SetStateAction } from "react";

import type {
  IFilter,
  IPermanentData,
  IPermanentValuesProps,
} from "components/Filter/types";

const setPermanentValues = ({
  permaValue,
  permaValues,
  setPermaValues,
}: IPermanentValuesProps): void => {
  setPermaValues?.(
    permaValues.map((permadata): IPermanentData => {
      if (permadata.id === permaValue.id) {
        return {
          ...permadata,
          checkValues: permaValue.checkValues,
          rangeValues: permaValue.rangeValues,
          value: permaValue.value,
        };
      }

      return permadata;
    })
  );
};

const rangeValueChangeHandler = <IData extends object>(
  id: string,
  filters: IFilter<IData>[],
  position: 0 | 1,
  setFilters: Dispatch<SetStateAction<IFilter<IData>[]>>,
  permaValues?: IPermanentData[],
  setPermaValues?: Dispatch<SetStateAction<IPermanentData[]>>
): ((event: React.ChangeEvent<HTMLInputElement>) => void) => {
  return (event: React.ChangeEvent<HTMLInputElement>): void => {
    setFilters(
      filters.map((filter): IFilter<IData> => {
        const value: [string, string] =
          position === 0
            ? [event.target.value, filter.rangeValues?.[1] ?? ""]
            : [filter.rangeValues?.[0] ?? "", event.target.value];

        if (filter.id === id) {
          const permaValue: IPermanentData = {
            checkValues: filter.checkValues,
            id,
            rangeValues: value,
            value: filter.value,
          };
          if (permaValues)
            setPermanentValues({ permaValue, permaValues, setPermaValues });

          return {
            ...filter,
            rangeValues: value,
          };
        }

        return filter;
      })
    );
  };
};

export { rangeValueChangeHandler, setPermanentValues };
