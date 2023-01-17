import React from "react";
import { useTranslation } from "react-i18next";

import { Breadcrumb } from "./Breadcrumb";
import { HelpButton } from "./HelpButton";
import { NewsWidget } from "./NewsWidget";
import { Searchbar } from "./Searchbar";
import { NavbarContainer, NavbarHeader, NavbarMenu } from "./styles";
import { TaskInfo } from "./Tasks";
import { TechnicalInfo } from "./TechnicalInfo";
import { UserProfile } from "./UserProfile";

import { Tooltip } from "components/Tooltip";
import { Can } from "utils/authz/Can";

interface INavbarProps {
  userRole: string | undefined;
}

export const Navbar: React.FC<INavbarProps> = ({
  userRole,
}: INavbarProps): JSX.Element => {
  const { t } = useTranslation();

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
            <TaskInfo />
          </li>
          <li>
            <Tooltip id={"navbar.newsTooltip.id"} tip={t("navbar.newsTooltip")}>
              <NewsWidget />
            </Tooltip>
          </li>
          <li>
            <HelpButton />
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
