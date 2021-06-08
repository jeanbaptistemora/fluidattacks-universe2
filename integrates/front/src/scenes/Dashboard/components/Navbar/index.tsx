import React from "react";
import { useTranslation } from "react-i18next";

import { Breadcrumb } from "./Breadcrumb";
import { HelpWidget } from "./HelpWidget";
import { NewsWidget } from "./NewsWidget";
import { Searchbar } from "./Searchbar";
import { NavbarContainer, NavbarHeader, NavbarMenu } from "./styles";
import { TechnicalInfo } from "./TechnicalInfo";
import { UserProfile } from "./UserProfile";

import { TooltipWrapper } from "components/TooltipWrapper";
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
            <TooltipWrapper
              id={"navbar.newsTooltip.id"}
              message={t("navbar.newsTooltip")}
            >
              <NewsWidget />
            </TooltipWrapper>
          </li>
          <li>
            <HelpWidget />
          </li>
          <li>
            <TechnicalInfo />
          </li>
          <li>
            <UserProfile userRole={userRole} />
          </li>
        </NavbarMenu>
      </NavbarContainer>
    </React.StrictMode>
  );
};
