import { faComment, faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";
import { useDetectClickOutside } from "react-detect-click-outside";
import { useTranslation } from "react-i18next";

import { DropdownButton, DropdownMenu, NavbarButton } from "../styles";
import { toggleZendesk } from "utils/widgets";

export const HelpWidget: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const [isDropdownOpen, setDropdownOpen] = useState(false);
  const toggleDropdown = useCallback((): void => {
    setDropdownOpen((currentValue): boolean => !currentValue);
  }, []);
  const ref = useDetectClickOutside({
    onTriggered: (): void => {
      setDropdownOpen(false);
    },
  });

  return (
    <div ref={ref}>
      <NavbarButton onClick={toggleDropdown}>
        <FontAwesomeIcon icon={faQuestionCircle} />
      </NavbarButton>
      {isDropdownOpen ? (
        <DropdownMenu>
          <li>
            <DropdownButton onClick={toggleZendesk}>
              <FontAwesomeIcon icon={faComment} />
              &nbsp;{t("navbar.help.chat")}
            </DropdownButton>
          </li>
        </DropdownMenu>
      ) : undefined}
    </div>
  );
};
