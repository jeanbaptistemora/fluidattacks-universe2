/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IGroupData {
  description: string;
  eventFormat: string;
  events: {
    eventStatus: string;
  }[];
  machine: string;
  squad: string;
  service: string;
  hasMachine: boolean;
  hasSquad: boolean;
  name: string;
  plan: string;
  responsible: string;
  subscription: string;
  userRole: string;
}

interface IOrganizationGroupsProps {
  organizationId: string;
}

interface IGetOrganizationGroups {
  organization: {
    groups: IGroupData[];
  };
}

export type { IGroupData, IOrganizationGroupsProps, IGetOrganizationGroups };
