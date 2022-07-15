import React from "react";
import type { ColumnDescription } from "react-bootstrap-table-next";

import { Tooltip } from "components/Tooltip";

export const tooltipFormatter = (
  column: ColumnDescription,
  colIndex: number,
  components: {
    sortElement: JSX.Element;
    filterElement: JSX.Element;
  }
): JSX.Element => (
  <Tooltip
    id={`headers.${column.text}.${colIndex}.help`}
    place={"top"}
    tip={column.tooltipDataField ?? ""}
  >
    <div className={"nowrap"}>
      {column.text}
      {components.sortElement}
    </div>
    {components.filterElement}
  </Tooltip>
);
