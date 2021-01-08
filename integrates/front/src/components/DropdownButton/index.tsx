/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles and props spreading in
  order to pass down props to react-bootstrap DropdownButton.
*/
import { MenuItem } from "./components/MenuItem";
import React from "react";
import type { StyledComponent } from "styled-components";
import style from "components/DropdownButton/index.css";
import styled from "styled-components";

interface IDropdownButtonProps {
  content: React.ReactNode;
  id: string;
  items: React.ReactNode;
}

const StyledDropdownButton: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "relative dib pa3",
})``;

const ItemsContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "absolute dn z-1",
})``;

const DropdownButton: React.FC<IDropdownButtonProps> = (
  props: Readonly<IDropdownButtonProps>
): JSX.Element => {
  const { content, id, items } = props;

  return (
    <StyledDropdownButton className={style.dropdownButton} id={id}>
      {content}
      <ItemsContainer className={style.itemsContainer}>{items}</ItemsContainer>
    </StyledDropdownButton>
  );
};

export { DropdownButton, MenuItem };
