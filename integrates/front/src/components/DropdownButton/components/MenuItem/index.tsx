/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles and props spreading in
  order to pass down props to react-bootstrap DropdownButton.
*/
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import style from "components/DropdownButton/index.css";

interface IMenuItemsProps {
  eventKey: string;
  onClick: (eventKey: string) => void;
  itemContent: React.ReactNode;
}

const StyledMenuItem: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs(
  ({
    className,
    type,
  }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: `ba br0 pa3 outline-0 justify-center ${className ?? ""}`,
    type: type ?? "button",
  })
)`
  height: 55px;
`;

const MenuItem: React.FC<IMenuItemsProps> = (
  props: Readonly<IMenuItemsProps>
): JSX.Element => {
  const { itemContent, eventKey, onClick } = props;

  function onClick1(): void {
    onClick(eventKey);
  }

  return (
    <StyledMenuItem className={style.menuItem} onClick={onClick1}>
      {itemContent}
    </StyledMenuItem>
  );
};

export { MenuItem };
