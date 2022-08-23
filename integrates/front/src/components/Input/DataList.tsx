import type { FC } from "react";
import React from "react";

interface IDataListProps {
  data: (number | string)[];
  id: string;
}

const DataList: FC<IDataListProps> = ({
  data,
  id,
}: Readonly<IDataListProps>): JSX.Element => (
  <datalist id={id}>
    {data.map(
      (suggestion): JSX.Element => (
        <option key={suggestion} value={suggestion}>
          {suggestion}
        </option>
      )
    )}
  </datalist>
);

export type { IDataListProps };
export { DataList };
