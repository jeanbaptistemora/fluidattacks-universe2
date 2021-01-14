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
  width: string;
}

const StyledDropdownButton: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `relative dib pa3 tc ${style.dropdownButton}`,
})``;

const ItemsContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `absolute dn z-1 ${style.itemsContainer}`,
})``;

const DropdownButton: React.FC<IDropdownButtonProps> = (
  props: Readonly<IDropdownButtonProps>
): JSX.Element => {
  const { content, id, items, width } = props;

  return (
    <StyledDropdownButton className={width} id={id}>
      {content}
      <ItemsContainer className={width}>{items}</ItemsContainer>
    </StyledDropdownButton>
  );
};

export { DropdownButton, MenuItem };
