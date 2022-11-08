/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { Dispatch, SetStateAction } from "react";

interface IFilter<IData extends object> {
  filterFn?:
    | "caseInsensitive"
    | "caseSensitive"
    | "includesInArray"
    | "includesInsensitive"
    | "includesSensitive";
  id: string;
  key: keyof IData | ((arg0: IData) => boolean);
  label?: string;
  rangeValues?: [string, string];
  selectOptions?:
    | { header: string; value: string }[]
    | string[]
    | ((arg0: IData[]) => { header: string; value: string }[])
    | ((arg0: IData[]) => string[]);
  type?: "dateRange" | "number" | "numberRange" | "select" | "text";
  value?: string;
}

interface IFilterComp<IData extends object> extends IFilter<IData> {
  key: keyof IData;
}

interface IFiltersProps<IData extends object> {
  dataset?: IData[];
  filters: IFilter<IData>[];
  setFilters: Dispatch<SetStateAction<IFilter<IData>[]>>;
}

export type { IFilter, IFilterComp, IFiltersProps };
