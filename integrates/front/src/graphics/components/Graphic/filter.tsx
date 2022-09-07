/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faFilter } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { Tooltip } from "components/Tooltip/index";
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
    <Tooltip
      id={"filter_button_tooltip"}
      tip={translate.t("analytics.buttonToolbar.filter.tooltip")}
    >
      <GraphicButton>
        <FontAwesomeIcon icon={faFilter} />
      </GraphicButton>
    </Tooltip>
    <Children>{children}</Children>
  </Dropdown>
);

export { DropdownFilter };
