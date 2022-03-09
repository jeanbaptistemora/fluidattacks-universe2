import React from "react";
import type { ColumnDescription } from "react-bootstrap-table-next";

import { TooltipWrapper } from "components/TooltipWrapper";

export const tooltipFormatter = (column: ColumnDescription): JSX.Element => (
  <TooltipWrapper
    id={`headers.${column.text}.help`}
    message={column.tooltipDataField ?? ""}
    placement={"top"}
  >
    <div className={"nowrap"}>{column.text}</div>
  </TooltipWrapper>
);
