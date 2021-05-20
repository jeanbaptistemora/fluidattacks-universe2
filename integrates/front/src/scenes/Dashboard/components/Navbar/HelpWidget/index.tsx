import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { NavbarButton } from "../styles";
import { toggleZendesk } from "utils/widgets";

export const HelpWidget: React.FC = (): JSX.Element => (
  <NavbarButton onClick={toggleZendesk}>
    <FontAwesomeIcon icon={faQuestionCircle} />
  </NavbarButton>
);
