import type { Dispatch, SetStateAction } from "react";

interface IFilter<IData extends object> {
  checkValues?: string[];
  filterFn?:
    | "caseInsensitive"
    | "caseSensitive"
    | "includesInArray"
    | "includesInsensitive"
    | "includesSensitive";
  id: string;
  key:
    | keyof IData
    | ((
        arg0: IData,
        value?: string,
        rangeValues?: [string, string]
      ) => boolean);
  label: string;
  rangeValues?: [string, string];
  selectOptions?:
    | ISelectedOptions[]
    | string[]
    | ((arg0: IData[]) => ISelectedOptions[])
    | ((arg0: IData[]) => string[]);
  type?:
    | "checkBoxes"
    | "dateRange"
    | "number"
    | "numberRange"
    | "select"
    | "text";
  value?: string;
}

interface ISelectedOptions {
  header: string;
  value: string;
}

interface IFilterComp<IData extends object> extends IFilter<IData> {
  key: keyof IData;
}

interface IPermanentData {
  checkValues?: string[];
  id: string;
  value?: string;
  rangeValues?: [string, string];
}

interface IPermanentValuesProps {
  permaValue: IPermanentData;
  permaValues: IPermanentData[];
  setPermaValues?: Dispatch<SetStateAction<IPermanentData[]>>;
}

interface IFiltersProps<IData extends object> {
  dataset?: IData[];
  permaset?: [IPermanentData[], Dispatch<SetStateAction<IPermanentData[]>>];
  filters: IFilter<IData>[];
  setFilters: Dispatch<SetStateAction<IFilter<IData>[]>>;
}

export type {
  IFilter,
  IFilterComp,
  IFiltersProps,
  IPermanentData,
  IPermanentValuesProps,
  ISelectedOptions,
};
