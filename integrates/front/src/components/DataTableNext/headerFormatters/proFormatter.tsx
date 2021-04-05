import React from "react";
import type { ReactElement } from "react";
import type { Column } from "react-bootstrap-table-next";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { Badge } from "components/Badge";

const BadgeContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "flex items-center justify-center relative",
})``;

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
    <BadgeContainer>
      <BadgeContainer>
        {column.text}
        <Badge>{"pro"}</Badge>
      </BadgeContainer>
      {sortElement}
    </BadgeContainer>
  );
};
