import type { Column } from "react-bootstrap-table-next";
import React from "react";
import type { ReactElement } from "react";
import { Row } from "styles/styledComponents";

export const filterFormatter: (
  column: Column,
  colIndex: number,
  components: Record<string, ReactElement>
) => JSX.Element = (
  column: Column,
  _colIndex: number,
  { filterElement, sortElement }: Record<string, ReactElement>
): JSX.Element => {
  return (
    <Row>
      <p>
        {column.text} {sortElement}
      </p>
      {filterElement}
    </Row>
  );
};
