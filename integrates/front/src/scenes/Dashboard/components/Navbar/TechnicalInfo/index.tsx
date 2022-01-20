import { faAngleDown, faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";
import { useDetectClickOutside } from "react-detect-click-outside";
import { useTranslation } from "react-i18next";

import { DropdownButton, DropdownMenu, NavbarButton } from "../styles";
import { ExternalLink } from "components/ExternalLink";
import {
  ASM_DEPLOYMENT_DATE,
  CI_COMMIT_SHA,
  CI_COMMIT_SHORT_SHA,
} from "utils/ctx";

export const TechnicalInfo: React.FC = (): JSX.Element => {
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
        <FontAwesomeIcon icon={faInfoCircle} />
        &nbsp;
        <FontAwesomeIcon icon={faAngleDown} size={"sm"} />
      </NavbarButton>
      {isDropdownOpen ? (
        <DropdownMenu>
          <li>
            <DropdownButton>
              <div>
                {t("info.commit")}&nbsp;
                <ExternalLink
                  href={`https://gitlab.com/fluidattacks/product/-/tree/${CI_COMMIT_SHA}`}
                >
                  {CI_COMMIT_SHORT_SHA}
                </ExternalLink>
              </div>
              <small>
                {t("info.deploymentDate")}&nbsp;
                {ASM_DEPLOYMENT_DATE}
              </small>
            </DropdownButton>
          </li>
        </DropdownMenu>
      ) : undefined}
    </div>
  );
};
