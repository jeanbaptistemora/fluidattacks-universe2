/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles and props spreading in
  order to pass down props to react-bootstrap DropdownButton.
*/
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { MenuItem } from "./components/MenuItem";

import style from "components/DropdownButton/index.css";

interface IDropdownButtonProps {
  content: React.ReactNode;
  id: string;
  items: React.ReactNode;
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
  const { content, id, items } = props;

  return (
    <StyledDropdownButton id={id}>
      {content}
      <ItemsContainer>{items}</ItemsContainer>
    </StyledDropdownButton>
  );
};

export { DropdownButton, MenuItem };
