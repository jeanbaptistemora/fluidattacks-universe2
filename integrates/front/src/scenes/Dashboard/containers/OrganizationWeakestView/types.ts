/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ApolloQueryResult, OperationVariables } from "@apollo/client";

import type { IGroups } from "scenes/Dashboard/types";

interface IIntegrationRepositoriesAttr {
  defaultBranch: string;
  lastCommitDate: string | null;
  url: string;
}

interface IOrganizationIntegrationRepositoriesAttr {
  organization: {
    integrationRepositories: IIntegrationRepositoriesAttr[];
  };
}

interface IPlusModalProps {
  groupNames: string[];
  isOpen: boolean;
  repository: IIntegrationRepositoriesAttr;
  organizationId: string;
  refetchRepositories: (
    variables?: Partial<OperationVariables> | undefined
  ) => Promise<ApolloQueryResult<IOrganizationIntegrationRepositoriesAttr>>;
  changePermissions: (groupName: string) => void;
  onClose: () => void;
}

interface IOrganizationWeakestProps {
  organizationId: string;
}

interface IOrganizationGroups {
  groups: IGroups[];
  name: string;
  permissions: string[];
}

export type {
  IIntegrationRepositoriesAttr,
  IPlusModalProps,
  IOrganizationIntegrationRepositoriesAttr,
  IOrganizationWeakestProps,
  IOrganizationGroups,
};
