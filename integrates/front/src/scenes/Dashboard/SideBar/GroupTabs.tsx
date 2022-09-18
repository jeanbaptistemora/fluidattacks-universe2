/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
import type { FC } from "react";
import React from "react";
import { useParams } from "react-router-dom";

import { SideBarTab } from "components/SideBar";

const GroupTabs: FC = (): JSX.Element => {
  const { group, org } = useParams<{ group: string; org: string }>();

  return (
    <SideBarTab to={`/orgs/${org}/groups/${group}/vulns`}>
      {"Vulnerabilities"}
    </SideBarTab>
  );
};

export { GroupTabs };
