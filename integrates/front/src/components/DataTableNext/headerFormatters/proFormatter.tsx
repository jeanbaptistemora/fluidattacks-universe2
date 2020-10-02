import { Badge } from "components/Badge";
import { Column } from "react-bootstrap-table-next";
import React, { ReactElement } from "react";
import styled, { StyledComponent } from "styled-components";

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
