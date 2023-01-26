import type { IFilter } from "../types";

interface IAppliedFilters {
  filters: IFilter<object>[];
  dataset?: object[];
  onClose: (filterToReset: IFilter<object>) => () => void;
}

export type { IAppliedFilters };
