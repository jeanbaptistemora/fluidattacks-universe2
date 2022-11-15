/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { faPlug } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
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
import { useHistory, useParams } from "react-router-dom";

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

import { GET_ORGANIZATION_CREDENTIALS } from "../OrganizationCredentialsView/queries";
import type { ICredentialsAttr } from "../OrganizationCredentialsView/types";
import type { IAction, IGroupAction } from "../Tasks/Vulnerabilities/types";
import { Button } from "components/Button";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { Tooltip } from "components/Tooltip";
import { Can } from "utils/authz/Can";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";

const formatDate: (date: Date | string | null | undefined) => string = (
  date: Date | string | null | undefined
): string => {
  if (date === undefined || date === null) {
    return "-";
  }

  const result: string = moment(date).format("YYYY-MM-DD hh:mm:ss");

  return result === "Invalid date" ? "-" : result;
};

export const OrganizationWeakest: React.FC<IOrganizationWeakestProps> = ({
  organizationId,
}: IOrganizationWeakestProps): JSX.Element => {
  const { t } = useTranslation();
  const { push } = useHistory();
  const { organizationName } = useParams<{ organizationName: string }>();

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

  const { data: credentialsData } = useQuery<{
    organization: { credentials: ICredentialsAttr[] };
  }>(GET_ORGANIZATION_CREDENTIALS, {
    onError: (errors: ApolloError): void => {
      errors.graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error(
          "Couldn't load organization credentials from weakest",
          error
        );
      });
    },
    variables: {
      organizationId,
    },
  });

  const credentialsAttrs = useMemo(
    (): ICredentialsAttr[] =>
      _.isUndefined(credentialsData)
        ? []
        : credentialsData.organization.credentials.filter(
            (credential: ICredentialsAttr): boolean => credential.isPat
          ),
    [credentialsData]
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
        repositoriesData.organization.integrationRepositories.map(
          (
            repository: IIntegrationRepositoriesAttr
          ): IIntegrationRepositoriesAttr => ({
            ...repository,
            lastCommitDate: formatDate(repository.lastCommitDate),
          })
        ),
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

  const onMoveToCredentials = useCallback((): void => {
    push(`/orgs/${organizationName}/credentials`);
  }, [organizationName, push]);

  return (
    <React.StrictMode>
      {credentialsAttrs.length === 0 && credentialsData !== undefined ? (
        <Can do={"api_mutations_add_credentials_mutate"}>
          <Tooltip
            disp={"inline-block"}
            id={"organization.tabs.weakest.buttons.add.tooltip.id"}
            tip={t("organization.tabs.weakest.buttons.add.tooltip")}
          >
            <Button
              id={"moveToCredentials"}
              onClick={onMoveToCredentials}
              variant={"secondary"}
            >
              <FontAwesomeIcon icon={faPlug} />
              &nbsp;
              {t("organization.tabs.weakest.buttons.add.text")}
            </Button>
          </Tooltip>
        </Can>
      ) : undefined}
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
