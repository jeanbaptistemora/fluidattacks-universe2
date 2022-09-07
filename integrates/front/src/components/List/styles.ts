/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

interface IListBoxProps {
  columns?: number;
}

interface IListItemProps {
  justify?: "center" | "end" | "start";
}

const ListBox = styled.div.attrs({
  className: "comp-list",
})<IListBoxProps>`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  > * {
    width: ${({ columns = 1 }): number => 100 / columns}%;
  }
`;

const ListItem = styled.div<IListItemProps>`
  align-items: center;
  display: flex;
  justify-content: ${({ justify = "center" }): string => justify};
`;

export type { IListBoxProps, IListItemProps };
export { ListBox, ListItem };
