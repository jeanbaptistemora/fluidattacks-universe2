import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { MenuButton } from "../styles";
import { toggleZendesk } from "utils/widgets";

export const HelpWidget: React.FC = (): JSX.Element => (
  <MenuButton onClick={toggleZendesk}>
    <FontAwesomeIcon icon={faQuestionCircle} />
  </MenuButton>
);
