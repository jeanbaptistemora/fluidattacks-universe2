import {
  faAngleDown,
  faComment,
  faHeadset,
  faQuestionCircle,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useContext, useState } from "react";
import { openPopupWidget } from "react-calendly";
import { useDetectClickOutside } from "react-detect-click-outside";
import { useTranslation } from "react-i18next";
import { useRouteMatch } from "react-router-dom";

import { UpgradeGroupsModal } from "./UpgradeGroupsModal";

import { DropdownButton, DropdownMenu, NavbarButton } from "../styles";
import { clickedPortal } from "../utils";
import type { IOrganizationGroups } from "scenes/Dashboard/types";
import { authContext } from "utils/auth";
import { toggleZendesk } from "utils/widgets";

interface IHelpWidgetProps {
  groups: IOrganizationGroups["groups"];
}

export const HelpWidget: React.FC<IHelpWidgetProps> = ({
  groups,
}: IHelpWidgetProps): JSX.Element => {
  const match = useRouteMatch<{ orgName: string; groupName: string }>(
    "/orgs/:orgName/groups/:groupName"
  );
  const { t } = useTranslation();
  const { userEmail, userName } = useContext(authContext);

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

  const [isUpgradeOpen, setIsUpgradeOpen] = useState(false);
  const closeUpgradeModal = useCallback((): void => {
    setIsUpgradeOpen(false);
  }, []);

  const openCalendly = useCallback((): void => {
    if (match) {
      const { groupName } = match.params;
      const currentGroup = groups.find(
        (group): boolean => group.name === groupName
      );
      const serviceAttributes =
        currentGroup === undefined ? [] : currentGroup.serviceAttributes;

      if (
        serviceAttributes.includes("has_squad") &&
        serviceAttributes.includes("is_continuous")
      ) {
        openPopupWidget({
          prefill: {
            customAnswers: { a1: groupName },
            email: userEmail,
            name: userName,
          },
          url: "https://calendly.com/fluidattacks/talk-to-an-expert",
        });
      } else {
        setIsUpgradeOpen(true);
      }
    }
  }, [groups, match, userEmail, userName]);

  return (
    <div ref={ref}>
      <NavbarButton onClick={toggleDropdown}>
        <FontAwesomeIcon icon={faQuestionCircle} />
        &nbsp;
        <FontAwesomeIcon icon={faAngleDown} size={"xs"} />
      </NavbarButton>
      {isDropdownOpen ? (
        <DropdownMenu>
          <li>
            <DropdownButton onClick={toggleZendesk}>
              <FontAwesomeIcon icon={faComment} />
              &nbsp;{t("navbar.help.chat")}
            </DropdownButton>
          </li>
          {match ? (
            <li>
              <DropdownButton onClick={openCalendly}>
                <FontAwesomeIcon icon={faHeadset} />
                &nbsp;{t("navbar.help.expert")}
              </DropdownButton>
              {isUpgradeOpen ? (
                <UpgradeGroupsModal
                  groups={groups}
                  onClose={closeUpgradeModal}
                />
              ) : undefined}
            </li>
          ) : undefined}
        </DropdownMenu>
      ) : undefined}
    </div>
  );
};
