/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ColumnDef } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { StrictMode, useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Button } from "components/Button";
import { Table } from "components/Table";
import { formatLinkHandler } from "components/Table/formatters/linkFormatter";
import { BaseStep, Tour } from "components/Tour/index";
import { AddGroupModal } from "scenes/Dashboard/components/AddGroupModal";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/OrganizationGroupsView/queries";
import type {
  IGetOrganizationGroups,
  IGroupData,
  IOrganizationGroupsProps,
} from "scenes/Dashboard/containers/OrganizationGroupsView/types";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const OrganizationGroups: React.FC<IOrganizationGroupsProps> = (
  props: IOrganizationGroupsProps
): JSX.Element => {
  const { organizationId } = props;
  const { organizationName } = useParams<{ organizationName: string }>();
  const { t } = useTranslation();

  // State management
  const [isGroupModalOpen, setIsGroupModalOpen] = useState(false);

  const user: Required<IAuthContext> = useContext(
    authContext as React.Context<Required<IAuthContext>>
  );

  const enableTour = !user.tours.newGroup;
  const [runTour, setRunTour] = useState(enableTour);

  const openNewGroupModal: () => void = useCallback((): void => {
    if (runTour) {
      setRunTour(false);
    }
    setIsGroupModalOpen(true);
  }, [runTour, setRunTour]);

  // GraphQL operations
  const { data, refetch: refetchGroups } = useQuery<IGetOrganizationGroups>(
    GET_ORGANIZATION_GROUPS,
    {
      onCompleted: (paramData: IGetOrganizationGroups): void => {
        if (_.isEmpty(paramData.organization.groups)) {
          Logger.warning("Empty groups", document.location.pathname);
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred loading organization groups",
            error
          );
        });
      },
      variables: {
        organizationId,
      },
    }
  );

  // State management
  const closeNewGroupModal: () => void = useCallback((): void => {
    if (enableTour) {
      user.setUser({
        tours: {
          newGroup: true,
          newRoot: user.tours.newRoot,
        },
        userEmail: user.userEmail,
        userIntPhone: user.userIntPhone,
        userName: user.userName,
      });
    }
    setIsGroupModalOpen(false);
    void refetchGroups();
  }, [enableTour, refetchGroups, user]);
  // Auxiliary functions
  const formatGroupData: (groupData: IGroupData[]) => IGroupData[] = (
    groupData: IGroupData[]
  ): IGroupData[] =>
    groupData.map((group: IGroupData): IGroupData => {
      const description: string = _.capitalize(group.description);
      const subscription: string = _.capitalize(group.subscription);
      const plan =
        subscription === "Oneshot"
          ? subscription
          : group.hasSquad
          ? "Squad"
          : "Machine";
      const vulnerabilities: string = `${group.openFindings} types found`;
      const eventFormat: string =
        _.isUndefined(group.events) || _.isEmpty(group.events)
          ? "None"
          : group.events.filter((event): boolean =>
              event.eventStatus.includes("CREATED")
            ).length > 0
          ? `${
              group.events.filter((event): boolean =>
                event.eventStatus.includes("CREATED")
              ).length
            } need(s) attention`
          : "None";

      return {
        ...group,
        description,
        eventFormat,
        plan,
        vulnerabilities,
      };
    });

  const tableHeaders: ColumnDef<IGroupData>[] = [
    {
      accessorKey: "name",
      cell: (cell): JSX.Element => {
        const link = `groups/${String(cell.getValue())}/vulns`;
        const text = cell.getValue<string>();

        return formatLinkHandler(link, text);
      },
      header: t("organization.tabs.groups.newGroup.name"),
    },
    {
      accessorKey: "description",
      enableColumnFilter: false,
      header: t("organization.tabs.groups.newGroup.description.text"),
    },
    {
      accessorKey: "plan",
      header: t("organization.tabs.groups.plan"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "vulnerabilities",
      enableColumnFilter: false,
      header: t("organization.tabs.groups.vulnerabilities"),
    },
    {
      accessorKey: "userRole",
      cell: (cell): string => {
        return t(`userModal.roles.${_.camelCase(cell.getValue())}`, {
          defaultValue: "-",
        });
      },
      enableColumnFilter: false,
      header: t("organization.tabs.groups.role"),
    },
    {
      accessorKey: "eventFormat",
      cell: (cell): JSX.Element => {
        const link = `groups/${String(cell.row.getValue("name"))}/events`;
        const text = cell.getValue<string>();

        return formatLinkHandler(link, text);
      },
      enableColumnFilter: false,
      header: t("organization.tabs.groups.newGroup.events.text"),
    },
  ];

  const dataset: IGroupData[] = data
    ? formatGroupData(data.organization.groups)
    : [];

  return (
    <StrictMode>
      {_.isUndefined(data) || _.isEmpty(data) ? undefined : (
        <Table
          columns={tableHeaders}
          data={dataset}
          enableColumnFilters={true}
          extraButtons={
            <Can do={"api_mutations_add_group_mutate"}>
              <Button
                id={"add-group"}
                onClick={openNewGroupModal}
                tooltip={
                  runTour
                    ? undefined
                    : t("organization.tabs.groups.newGroup.new.tooltip")
                }
                variant={"primary"}
              >
                <FontAwesomeIcon icon={faPlus} />
                &nbsp;
                {t("organization.tabs.groups.newGroup.new.text")}
              </Button>
            </Can>
          }
          id={"tblGroups"}
        />
      )}
      {isGroupModalOpen ? (
        <AddGroupModal
          isOpen={true}
          onClose={closeNewGroupModal}
          organization={organizationName}
          runTour={enableTour}
        />
      ) : undefined}
      {runTour ? (
        <Tour
          run={false}
          steps={[
            {
              ...BaseStep,
              content: t("tours.addGroup.addButton"),
              disableBeacon: true,
              hideFooter: true,
              target: "#add-group",
            },
          ]}
        />
      ) : undefined}
    </StrictMode>
  );
};

export { OrganizationGroups };
