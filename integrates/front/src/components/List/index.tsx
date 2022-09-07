/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint @typescript-eslint/no-explicit-any:0 */
import React from "react";

import type { IListBoxProps, IListItemProps } from "./styles";
import { ListBox, ListItem } from "./styles";

interface IListProps<T = any> extends IListBoxProps, IListItemProps {
  getKey: (el: T) => React.Key;
  items: T[];
  render: (el: T) => JSX.Element;
}

const List: React.FC<IListProps> = ({
  columns = 1,
  getKey,
  items,
  justify = "center",
  render,
}: Readonly<IListProps>): JSX.Element => (
  <ListBox columns={Math.max(columns, 1)}>
    {items.map(
      (el: any): JSX.Element => (
        <ListItem justify={justify} key={getKey(el)}>
          {render(el)}
        </ListItem>
      )
    )}
  </ListBox>
);

export type { IListProps };
export { List };
