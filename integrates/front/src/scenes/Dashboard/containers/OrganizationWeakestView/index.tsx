/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import type { ColumnDef } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import moment from "moment";
import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { useTranslation } from "react-i18next";

import { PlusModal } from "./modal";
import { plusFormatter } from "./plusFormatter";
import {
  GET_ORGANIZATION_GROUPS,
  GET_ORGANIZATION_INTEGRATION_REPOSITORIES,
} from "./queries";
import type {
  IIntegrationRepositoriesAttr,
  IOrganizationGroups,
  IOrganizationIntegrationRepositoriesAttr,
  IOrganizationWeakestProps,
} from "./types";

import type { IAction, IGroupAction } from "../Tasks/Vulnerabilities/types";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";

const formatDate: (date: Date | undefined) => string = (
  date: Date | undefined
): string => {
  if (_.isUndefined(date)) {
    return "";
  }

  return moment(date).format("YYYY-MM-DD hh:mm:ss");
};

export const OrganizationWeakest: React.FC<IOrganizationWeakestProps> = ({
  organizationId,
}: IOrganizationWeakestProps): JSX.Element => {
  const { t } = useTranslation();

  const attributesContext: PureAbility<string> = useContext(authzGroupContext);
  const permissionsContext: PureAbility<string> = useContext(
    authzPermissionsContext
  );

  const [selectedRow, setSelectedRow] =
    useState<IIntegrationRepositoriesAttr>();
  const [isOpen, setIsOpen] = useState<boolean>(false);

  // GraphQl queries
  const { data: repositoriesData, refetch: refetchRepositories } =
    useQuery<IOrganizationIntegrationRepositoriesAttr>(
      GET_ORGANIZATION_INTEGRATION_REPOSITORIES,
      {
        onError: ({ graphQLErrors }: ApolloError): void => {
          graphQLErrors.forEach((error: GraphQLError): void => {
            Logger.error(
              "Couldn't load organization integration repositories",
              error
            );
          });
        },
        variables: {
          organizationId,
        },
      }
    );

  const { data: groupsData } = useQuery<{ organization: IOrganizationGroups }>(
    GET_ORGANIZATION_GROUPS,
    {
      fetchPolicy: "cache-first",
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          Logger.warning("An error occurred fetching user groups", error);
        });
      },
      variables: {
        organizationId,
      },
    }
  );

  const groupNames = useMemo(
    (): string[] =>
      _.isUndefined(groupsData)
        ? []
        : groupsData.organization.groups.reduce(
            (previousValue: string[], group): string[] => {
              return group.permissions.includes(
                "api_mutations_add_git_root_mutate"
              ) && group.serviceAttributes.includes("has_service_white")
                ? [...previousValue, group.name]
                : previousValue;
            },
            []
          ),
    [groupsData]
  );

  const integrationRepositories = _.isUndefined(repositoriesData)
    ? []
    : _.orderBy(
        repositoriesData.organization.integrationRepositories,
        "lastCommitDate",
        "desc"
      );

  // Table config
  const tableColumns: ColumnDef<IIntegrationRepositoriesAttr>[] = [
    {
      accessorKey: "url",
      header: t("organization.tabs.weakest.table.url"),
    },
    {
      accessorKey: "lastCommitDate",
      cell: (cell: ICellHelper<IIntegrationRepositoriesAttr>): string =>
        formatDate(cell.getValue()),
      header: t("organization.tabs.weakest.table.lastCommitDate"),
    },
  ];
  const handlePlusRoot = useCallback(
    (repository: IIntegrationRepositoriesAttr | undefined): void => {
      if (repository !== undefined) {
        setIsOpen(true);
        setSelectedRow(repository);
      }
    },
    []
  );

  const onCloseModal: () => void = useCallback((): void => {
    setIsOpen(false);
  }, []);

  const plusColumn: ColumnDef<IIntegrationRepositoriesAttr>[] = [
    {
      accessorKey: "defaultBranch",
      cell: (cell: ICellHelper<IIntegrationRepositoriesAttr>): JSX.Element =>
        plusFormatter(cell.row.original, handlePlusRoot),
      header: t("organization.tabs.weakest.table.action"),
    },
  ];
  const onGroupChange: () => void = (): void => {
    attributesContext.update([]);
    permissionsContext.update([]);
    if (groupsData !== undefined) {
      const groupsServicesAttributes: IOrganizationGroups["groups"] =
        groupsData.organization.groups.reduce(
          (
            previousValue: IOrganizationGroups["groups"],
            currentValue
          ): IOrganizationGroups["groups"] => [
            ...previousValue,
            ...(currentValue.serviceAttributes.includes("has_service_white")
              ? [currentValue]
              : []),
          ],
          []
        );

      const currentAttributes: string[] = Array.from(
        new Set(
          groupsServicesAttributes.reduce(
            (previous: string[], current): string[] => [
              ...previous,
              ...current.serviceAttributes,
            ],
            []
          )
        )
      );
      if (currentAttributes.length > 0) {
        attributesContext.update(
          currentAttributes.map((action: string): IAction => ({ action }))
        );
      }
      permissionsContext.update(
        groupsData.organization.permissions.map(
          (action: string): IAction => ({ action })
        )
      );
    }
  };

  const changeOrganizationPermissions = useCallback((): void => {
    if (groupsData !== undefined) {
      permissionsContext.update(
        groupsData.organization.permissions.map(
          (action: string): IAction => ({ action })
        )
      );
    }
  }, [groupsData, permissionsContext]);

  const changeGroupPermissions = useCallback(
    (groupName: string): void => {
      permissionsContext.update([]);
      attributesContext.update([]);
      if (groupsData !== undefined) {
        const recordPermissions: IGroupAction[] =
          groupsData.organization.groups.map(
            (group: IOrganizationGroups["groups"][0]): IGroupAction => ({
              actions: group.permissions.map(
                (action: string): IAction => ({
                  action,
                })
              ),
              groupName: group.name,
            })
          );
        const filteredPermissions: IGroupAction[] = recordPermissions.filter(
          (recordPermission: IGroupAction): boolean =>
            recordPermission.groupName.toLowerCase() === groupName.toLowerCase()
        );
        if (filteredPermissions.length > 0) {
          permissionsContext.update(filteredPermissions[0].actions);
        }

        const recordServiceAttributes: IGroupAction[] =
          groupsData.organization.groups.map(
            (group: IOrganizationGroups["groups"][0]): IGroupAction => ({
              actions: group.serviceAttributes.map(
                (action: string): IAction => ({
                  action,
                })
              ),
              groupName: group.name,
            })
          );
        const filteredServiceAttributes: IGroupAction[] =
          recordServiceAttributes.filter(
            (record: IGroupAction): boolean =>
              record.groupName.toLowerCase() === groupName.toLowerCase()
          );
        if (filteredServiceAttributes.length > 0) {
          attributesContext.update(filteredServiceAttributes[0].actions);
        }
      }
    },
    [attributesContext, permissionsContext, groupsData]
  );

  useEffect(onGroupChange, [
    attributesContext,
    permissionsContext,
    groupsData,
    repositoriesData,
  ]);

  return (
    <React.StrictMode>
      <Table
        columns={[
          ...tableColumns,
          ...(groupNames.length > 0 ? plusColumn : []),
        ]}
        data={integrationRepositories}
        id={"tblOrganizationCredentials"}
      />
      {selectedRow ? (
        <PlusModal
          changeGroupPermissions={changeGroupPermissions}
          changeOrganizationPermissions={changeOrganizationPermissions}
          groupNames={groupNames}
          isOpen={isOpen}
          onClose={onCloseModal}
          organizationId={organizationId}
          refetchRepositories={refetchRepositories}
          repository={selectedRow}
        />
      ) : undefined}
    </React.StrictMode>
  );
};
