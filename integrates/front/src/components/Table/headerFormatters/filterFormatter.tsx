import React from "react";
import type { ReactElement } from "react";
import type { ColumnDescription } from "react-bootstrap-table-next";

import { Flex } from "styles/styledComponents";

export const filterFormatter = (
  column: ColumnDescription,
  _colIndex: number,
  { filterElement, sortElement }: Record<string, ReactElement>
): JSX.Element => {
  return (
    <React.StrictMode>
      <Flex>
        <Flex>{column.text}</Flex>
        {sortElement}
      </Flex>
      <Flex>{filterElement}</Flex>
    </React.StrictMode>
  );
};
