import React from "react";
import { useTranslation } from "react-i18next";

import { Breadcrumb } from "./Breadcrumb";
import { HelpButton } from "./HelpButton";
import { NewsWidget } from "./NewsWidget";
import { Searchbar } from "./Searchbar";
import { TaskInfo } from "./Tasks";
import { TechnicalInfo } from "./TechnicalInfo";
import { UserProfile } from "./UserProfile";

import { NavBar } from "components/NavBar";
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
    <NavBar header={<Breadcrumb />} variant={"light"}>
      <Can do={"front_can_use_groups_searchbar"}>
        <Searchbar />
      </Can>
      <TaskInfo />
      <Tooltip id={"navbar.newsTooltip.id"} tip={t("navbar.newsTooltip")}>
        <NewsWidget />
      </Tooltip>
      <HelpButton />
      <TechnicalInfo />
      <UserProfile userRole={userRole} />
    </NavBar>
  );
};
