import { faFilter } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { TooltipWrapper } from "components/TooltipWrapper/index";
import styles from "graphics/components/Graphic/index.css";
import { GraphicButton } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

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
    <TooltipWrapper
      id={"filter_button_tooltip"}
      message={translate.t("analytics.buttonToolbar.filter.tooltip")}
    >
      <GraphicButton>
        <FontAwesomeIcon icon={faFilter} />
      </GraphicButton>
    </TooltipWrapper>
    <Children>{children}</Children>
  </Dropdown>
);

export { DropdownFilter };
