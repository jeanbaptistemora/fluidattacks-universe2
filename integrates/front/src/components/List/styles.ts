import styled from "styled-components";

interface IListBoxProps {
  columns: number;
}

interface IListItemProps {
  justify: "center" | "end" | "start";
}

const ListBox = styled.div.attrs({
  className: "comp-list",
})<IListBoxProps>`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  > * {
    width: ${({ columns }): number => 100 / columns}%;
  }
`;

const ListItem = styled.div<IListItemProps>`
  align-items: center;
  display: flex;
  justify-content: ${({ justify }): string => justify};
`;

export type { IListBoxProps, IListItemProps };
export { ListBox, ListItem };
