import React from "react";

import { Item, Container as ListContainer } from "./styles";

import type { IContainerProps } from "components/Container";
import { Container } from "components/Container";

type TItem = TItem[] | boolean | number | string | undefined;

interface IItemProps extends Record<string, IItemProps[] | TItem> {
  id: React.Key;
}

interface IListProps<T = IItemProps> extends IContainerProps {
  columns: number;
  items: T[];
  render: (el: T) => JSX.Element;
}

const List: React.FC<IListProps> = ({
  columns = 1,
  height,
  items,
  margin,
  maxHeight,
  maxWidth,
  minHeight,
  minWidth,
  padding,
  render,
  scroll,
  width,
}: Readonly<IListProps>): JSX.Element => (
  <Container
    height={height}
    margin={margin}
    maxHeight={maxHeight}
    maxWidth={maxWidth}
    minHeight={minHeight}
    minWidth={minWidth}
    padding={padding}
    scroll={scroll}
    width={width}
  >
    <ListContainer columns={Math.max(columns, 1)}>
      {items.map(
        (el: IItemProps): JSX.Element => (
          <Item key={el.id}>{render(el)}</Item>
        )
      )}
    </ListContainer>
  </Container>
);

export type { IItemProps, IListProps };
export { List };
