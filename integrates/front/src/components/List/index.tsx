import React from "react";

import type { IListItemProps } from "./styles";
import { ListBox, ListItem } from "./styles";

import type { IContainerProps } from "components/Container";

type TItem = TItem[] | boolean | number | string | undefined;

interface IItemProps extends Record<string, IItemProps[] | TItem> {
  id: React.Key;
}

interface IListProps<T = IItemProps> extends IContainerProps, IListItemProps {
  columns: number;
  items: T[];
  render: (el: T) => JSX.Element;
}

const List: React.FC<IListProps> = ({
  columns = 1,
  items,
  justify = "center",
  render,
}: Readonly<IListProps>): JSX.Element => (
  <ListBox columns={Math.max(columns, 1)}>
    {items.map(
      (el: IItemProps): JSX.Element => (
        <ListItem justify={justify} key={el.id}>
          {render(el)}
        </ListItem>
      )
    )}
  </ListBox>
);

export type { IItemProps, IListProps };
export { List };
