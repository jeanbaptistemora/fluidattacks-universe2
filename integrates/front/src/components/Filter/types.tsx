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
    | { header: string; value: string }[]
    | string[]
    | ((arg0: IData[]) => { header: string; value: string }[])
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

interface IFilterComp<IData extends object> extends IFilter<IData> {
  key: keyof IData;
}

interface IPermanentData {
  checkValues?: string[];
  id: string;
  value?: string;
  rangeValues?: [string, string];
}

interface IFiltersProps<IData extends object> {
  dataset?: IData[];
  permaset?: [IPermanentData[], Dispatch<SetStateAction<IPermanentData[]>>];
  filters: IFilter<IData>[];
  setFilters: Dispatch<SetStateAction<IFilter<IData>[]>>;
}

export type { IFilter, IFilterComp, IFiltersProps, IPermanentData };
