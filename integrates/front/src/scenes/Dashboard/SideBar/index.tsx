/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
import { faHome } from "@fortawesome/free-solid-svg-icons";
import type { FC } from "react";
import React, { useContext } from "react";
import { Route } from "react-router-dom";

import { OrganizationTabs } from "./OrganizationTabs";

import { Sidebar } from "../components/Sidebar";
import { SideBar, SideBarTab } from "components/SideBar";
import { featurePreviewContext } from "utils/featurePreview";

const DashboardSideBar: FC = (): JSX.Element => {
  const { featurePreview } = useContext(featurePreviewContext);

  return featurePreview ? (
    <SideBar>
      <SideBarTab icon={faHome} to={"/home"}>
        {"Home"}
      </SideBarTab>
      <Route path={"/orgs/:org/"}>
        <OrganizationTabs />
      </Route>
    </SideBar>
  ) : (
    <Sidebar />
  );
};

export { DashboardSideBar };
