import React from "react";
import { useTranslation } from "react-i18next";

import { Breadcrumb } from "./Breadcrumb";
import { HelpWidget } from "./HelpWidget";
import { NewsWidget } from "./NewsWidget";
import { Searchbar } from "./Searchbar";
import { NavbarContainer, NavbarHeader, NavbarMenu } from "./styles";
import { TaskInfo } from "./Tasks";
import { TechnicalInfo } from "./TechnicalInfo";
import { UserProfile } from "./UserProfile";

import { TooltipWrapper } from "components/TooltipWrapper";
import type {
  IGetMeVulnerabilitiesAssigned,
  IGetUserOrganizationsGroups,
  IOrganizationGroups,
} from "scenes/Dashboard/types";
import { Can } from "utils/authz/Can";

interface INavbarProps {
  userRole: string | undefined;
  userData: IGetUserOrganizationsGroups | undefined;
  meVulnerabilitiesAssigned: IGetMeVulnerabilitiesAssigned | undefined;
}

export const Navbar: React.FC<INavbarProps> = ({
  userRole,
  userData,
  meVulnerabilitiesAssigned,
}: INavbarProps): JSX.Element => {
  const { t } = useTranslation();
  const groups =
    userData === undefined
      ? []
      : userData.me.organizations.reduce(
          (
            previousValue: IOrganizationGroups["groups"],
            currentValue
          ): IOrganizationGroups["groups"] => [
            ...previousValue,
            ...currentValue.groups,
          ],
          []
        );

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
            <TaskInfo meVulnerabilitiesAssigned={meVulnerabilitiesAssigned} />
          </li>
          <li>
            <TechnicalInfo />
          </li>
          <li>
            <HelpWidget groups={groups} />
          </li>
          <li>
            <UserProfile userRole={userRole} />
          </li>
        </NavbarMenu>
      </NavbarContainer>
    </React.StrictMode>
  );
};
