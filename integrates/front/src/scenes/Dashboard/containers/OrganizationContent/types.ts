/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IOrganizationContent {
  setUserRole: (userRole: string | undefined) => void;
}

interface IOrganizationPermission {
  organization: {
    permissions: string[];
    userRole: string | undefined;
  };
}

interface IGetOrganizationId {
  organizationId: {
    id: string;
    name: string;
  };
}

interface IGetUserPortfolios {
  me: {
    tags: {
      name: string;
      groups: {
        name: string;
      }[];
    }[];
    userEmail: string;
  };
}

export type {
  IGetOrganizationId,
  IGetUserPortfolios,
  IOrganizationContent,
  IOrganizationPermission,
};
