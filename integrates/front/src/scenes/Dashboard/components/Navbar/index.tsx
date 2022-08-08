import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Breadcrumb } from "./Breadcrumb";
import { HelpModal } from "./HelpModal";
import { NewsWidget } from "./NewsWidget";
import { Searchbar } from "./Searchbar";
import { NavbarContainer, NavbarHeader, NavbarMenu } from "./styles";
import { TaskInfo } from "./Tasks";
import { TechnicalInfo } from "./TechnicalInfo";
import { UserProfile } from "./UserProfile";

import { Button } from "components/Button";
import { useShow } from "components/Modal";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import { Can } from "utils/authz/Can";

interface INavbarProps {
  userRole: string | undefined;
}

export const Navbar: React.FC<INavbarProps> = ({
  userRole,
}: INavbarProps): JSX.Element => {
  const { t } = useTranslation();
  const [show, open, close] = useShow();

  return (
    <React.StrictMode>
      <NavbarContainer id={"navbar"}>
        <NavbarHeader>
          <Breadcrumb />
        </NavbarHeader>
        <NavbarMenu>
          <Can do={"front_can_use_groups_searchbar"}>
            <li>
              <Searchbar />
            </li>
          </Can>
          <li>
            <Tooltip id={"navbar.newsTooltip.id"} tip={t("navbar.newsTooltip")}>
              <NewsWidget />
            </Tooltip>
          </li>
          <li>
            <TaskInfo />
          </li>
          <li>
            <Button onClick={open} size={"sm"}>
              <Text size={4}>
                <FontAwesomeIcon icon={faQuestionCircle} />
              </Text>
            </Button>
            <HelpModal onClose={close} open={show} />
          </li>
          <li>
            <TechnicalInfo />
          </li>
          <li id={"navbar-user-profile"}>
            <UserProfile userRole={userRole} />
          </li>
        </NavbarMenu>
      </NavbarContainer>
    </React.StrictMode>
  );
};
