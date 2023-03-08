/* eslint @typescript-eslint/no-explicit-any:0 */
import type { ISelectedOptions } from "../types";

interface IFilter {
  id: string;
  label: string;
  onChange: (id: string, value: any) => void;
  checkValues?: string[];
  mappedOptions?: ISelectedOptions[];
  value?: string;
  numberRangeValues?: [string, string];
}

export type { IFilter };
