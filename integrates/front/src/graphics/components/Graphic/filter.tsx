import { faFilter } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import styles from "graphics/components/Graphic/index.css";
import { GraphicButton } from "styles/styledComponents";

interface IDropdownFilterProps {
  children: React.ReactNode;
}

const Dropdown: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `relative dib tc ${styles.dropdownFilter}`,
})``;

const Children: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `absolute dn f7 z-1 ${styles.childrenContainer}`,
})``;

const DropdownFilter: React.FC<IDropdownFilterProps> = ({
  children,
}: IDropdownFilterProps): JSX.Element => (
  <Dropdown>
    <GraphicButton>
      <FontAwesomeIcon icon={faFilter} />
    </GraphicButton>
    <Children>{children}</Children>
  </Dropdown>
);

export { DropdownFilter };
