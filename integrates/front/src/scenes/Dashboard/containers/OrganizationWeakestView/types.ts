import type { ApolloQueryResult, OperationVariables } from "@apollo/client";
import type { ExecutionResult } from "graphql";

import type { IGroups } from "scenes/Dashboard/types";

interface IAddGitRootMutation {
  addGitRoot: {
    success: boolean;
  };
}

type AddGitRootResult = ExecutionResult<IAddGitRootMutation>;

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
  IAddGitRootMutation,
  AddGitRootResult,
};
