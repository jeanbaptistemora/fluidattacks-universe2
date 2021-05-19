import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { toggleZendesk } from "utils/widgets";

export const HelpWidget: React.FC = (): JSX.Element => (
  <div>
    <FontAwesomeIcon icon={faQuestionCircle} onClick={toggleZendesk} />
  </div>
);
