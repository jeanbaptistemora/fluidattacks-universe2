import React, { useRef } from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { MenuItem } from "./components/MenuItem";

import style from "components/DropdownButton/index.css";

interface IDropdownButtonProps {
  content: React.ReactNode;
  id: string;
  items: React.ReactNode;
  scrollInto: boolean;
}

const StyledDropdownButton: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `relative dib tc ${style.dropdownButton}`,
})``;

const ItemsContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `absolute dn z-1 ${style.itemsContainer}`,
})``;

const DropdownButton: React.FC<IDropdownButtonProps> = ({
  content,
  id,
  items,
  scrollInto,
}: IDropdownButtonProps): JSX.Element => {
  const dropdownRef: React.MutableRefObject<HTMLDivElement | null> =
    useRef(null);

  function onMouseEnter(): void {
    if (dropdownRef.current !== null && scrollInto) {
      dropdownRef.current.scrollIntoView({
        behavior: "auto",
        block: "center",
      });
    }
  }

  return (
    <StyledDropdownButton id={id} onMouseEnter={onMouseEnter} ref={dropdownRef}>
      {content}
      <ItemsContainer>{items}</ItemsContainer>
    </StyledDropdownButton>
  );
};

export { DropdownButton, MenuItem };
