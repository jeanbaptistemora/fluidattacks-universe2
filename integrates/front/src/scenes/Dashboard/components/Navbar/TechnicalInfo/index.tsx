import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";
import { useDetectClickOutside } from "react-detect-click-outside";
import { useTranslation } from "react-i18next";

import { clickedPortal } from "../utils";
import { ButtonOpacity } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Menu, MenuItem } from "components/Menu";
import {
  ASM_DEPLOYMENT_DATE,
  CI_COMMIT_SHA,
  CI_COMMIT_SHORT_SHA,
} from "utils/ctx";

export const TechnicalInfo: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const toggleDropdown = useCallback((): void => {
    setIsDropdownOpen((currentValue): boolean => !currentValue);
  }, []);
  const ref = useDetectClickOutside({
    onTriggered: (event): void => {
      // Exclude clicks in portals to prevent modals from closing the dropdown
      if (!clickedPortal(event)) {
        setIsDropdownOpen(false);
      }
    },
  });

  return (
    <div ref={ref}>
      <ButtonOpacity onClick={toggleDropdown}>
        <FontAwesomeIcon color={"#2e2e38"} icon={faInfoCircle} />
      </ButtonOpacity>
      {isDropdownOpen ? (
        <Menu align={"right"}>
          <MenuItem>
            <button>
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
            </button>
          </MenuItem>
        </Menu>
      ) : undefined}
    </div>
  );
};
