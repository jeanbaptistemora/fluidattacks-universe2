import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import styled from "styled-components";

import { toggleZendesk } from "utils/widgets";

const StyledWidget = styled.div.attrs({
  className: "pointer red",
})``;

export const HelpWidget: React.FC = (): JSX.Element => (
  <StyledWidget>
    <FontAwesomeIcon icon={faQuestionCircle} onClick={toggleZendesk} />
  </StyledWidget>
);
