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

interface IPlusModalProps {
  groupNames: string[];
  isOpen: boolean;
  repository: IIntegrationRepositoriesAttr;
  organizationId: string;
  refetchRepositories: (
    variables?: Partial<OperationVariables> | undefined
  ) => Promise<ApolloQueryResult<IOrganizationIntegrationRepositoriesAttr>>;
  changeGroupPermissions: (groupName: string) => void;
  changeOrganizationPermissions: () => void;
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

interface IIntegrationRepositoriesEdge {
  node: IIntegrationRepositoriesAttr;
}

interface IIntegrationRepositoriesConnection {
  edges: IIntegrationRepositoriesEdge[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string;
  };
}

interface IOrganizationIntegrationRepositoriesAttr {
  organization: {
    integrationRepositoriesConnection: IIntegrationRepositoriesConnection;
  };
}

export type {
  IIntegrationRepositoriesConnection,
  IIntegrationRepositoriesEdge,
  IIntegrationRepositoriesAttr,
  IPlusModalProps,
  IOrganizationIntegrationRepositoriesAttr,
  IOrganizationWeakestProps,
  IOrganizationGroups,
};
