/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
import {
  faChartColumn,
  faHome,
  faShield,
} from "@fortawesome/free-solid-svg-icons";
import type { FC } from "react";
import React, { useContext } from "react";
import { Route, useParams } from "react-router-dom";

import { GroupTabs } from "./GroupTabs";

import { Sidebar } from "../components/Sidebar";
import { SideBar, SideBarSubTabs, SideBarTab } from "components/SideBar";
import { featurePreviewContext } from "utils/featurePreview";

const DashboardSideBar: FC = (): JSX.Element => {
  const { featurePreview } = useContext(featurePreviewContext);
  const { org } = useParams<{ org: string }>();

  return featurePreview ? (
    <SideBar>
      <SideBarTab icon={faHome} to={"/home"}>
        {"Home"}
      </SideBarTab>
      <SideBarSubTabs>
        <SideBarTab key={"groups"} to={`/orgs/${org}/groups`}>
          {"Groups"}
        </SideBarTab>
        <Route key={"groupRoutes"} path={"/orgs/:org/groups/:group/"}>
          <GroupTabs />
        </Route>
      </SideBarSubTabs>
      <SideBarTab icon={faChartColumn} to={`/orgs/${org}/analytics`}>
        {"Analytics"}
      </SideBarTab>
      <SideBarTab icon={faShield} to={`/orgs/${org}/policies`}>
        {"Policies"}
      </SideBarTab>
    </SideBar>
  ) : (
    <Sidebar />
  );
};

export { DashboardSideBar };
