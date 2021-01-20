import type { Column } from "react-bootstrap-table-next";
import { Flex } from "styles/styledComponents";
import React from "react";
import type { ReactElement } from "react";

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
    <React.StrictMode>
      <Flex>
        <Flex>{column.text}</Flex>
        {sortElement}
      </Flex>
      <Flex>{filterElement}</Flex>
    </React.StrictMode>
  );
};
