import { faFilter } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import styled from "styled-components";

import { Tooltip } from "components/Tooltip/index";
import { GraphicButton } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

interface IDropdownFilterProps {
  children: React.ReactNode;
}

const Children = styled.div.attrs({
  className: `absolute dn f7 word-normal z-1`,
})``;

const Dropdown = styled.div.attrs({
  className: "br0 dib pointer relative tc ws-normal",
})`
  :hover ${Children} {
    background-color: #eee;
    display: block;
  }
`;

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
