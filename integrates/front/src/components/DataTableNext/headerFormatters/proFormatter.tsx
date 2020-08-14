import { Badge } from "../../Badge";
import { Column } from "react-bootstrap-table-next";
import { default as style } from "../index.css";
import React, { ReactElement } from "react";

export const proFormatter: (
  column: Column,
  colIndex: number,
  components: Record<string, ReactElement>
) => JSX.Element = (
  column: Column,
  _colIndex: number,
  { sortElement }: Record<string, ReactElement>
): JSX.Element => {
  return (
    <div className={style.plusFormatter}>
      <div>
        {column.text}
        <Badge>{"pro"}</Badge>
      </div>
      {sortElement}
    </div>
  );
};
