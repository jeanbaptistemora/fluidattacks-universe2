/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IUserOrgs {
  me: {
    organizations: { name: string }[];
    userEmail: string;
  };
}

interface IUserOrganizationGroupNames {
  organization: {
    groups: { name: string }[];
  };
}

interface IUserTags {
  me: {
    tags: { name: string }[];
    userEmail: string;
  };
}

interface IFindingTitle {
  finding: {
    title: string;
  };
}

export type {
  IFindingTitle,
  IUserOrgs,
  IUserOrganizationGroupNames,
  IUserTags,
};
