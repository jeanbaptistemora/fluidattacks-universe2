import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ColumnDef } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Button } from "components/Button";
import { Tables } from "components/TableNew";
import { formatLinkHandler } from "components/TableNew/formatters/linkFormatter";
import type { ICellHelper } from "components/TableNew/types";
import { Tooltip } from "components/Tooltip/index";
import { BaseStep, Tour } from "components/Tour/index";
import { AddGroupModal } from "scenes/Dashboard/components/AddGroupModal";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/OrganizationGroupsView/queries";
import type {
  IGetOrganizationGroups,
  IGroupData,
  IOrganizationGroupsProps,
} from "scenes/Dashboard/containers/OrganizationGroupsView/types";
import { Row } from "styles/styledComponents";
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
      const name: string = group.name.toUpperCase();
      const description: string = _.capitalize(group.description);
      const subscription: string = _.capitalize(group.subscription);
      const plan =
        subscription === "Oneshot"
          ? subscription
          : group.hasSquad
          ? "Squad"
          : "Machine";
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
        name,
        plan,
      };
    });

  const tableHeaders: ColumnDef<IGroupData>[] = [
    {
      accessorKey: "name",
      cell: (cell: ICellHelper<IGroupData>): JSX.Element => {
        const link: string = `${String(cell.getValue())}/vulns`;
        const text: string = cell.getValue();

        return formatLinkHandler(link, text);
      },
      header: t("organization.tabs.groups.newGroup.name"),
    },
    {
      accessorKey: "description",
      header: t("organization.tabs.groups.newGroup.description.text"),
    },
    { accessorKey: "plan", header: t("organization.tabs.groups.plan") },
    {
      accessorKey: "userRole",
      cell: (cell: ICellHelper<IGroupData>): string => {
        return t(`userModal.roles.${_.camelCase(cell.getValue())}`, {
          defaultValue: "-",
        });
      },
      header: t("organization.tabs.groups.role"),
    },
    {
      accessorKey: "eventFormat",
      cell: (cell: ICellHelper<IGroupData>): JSX.Element => {
        const link: string = `${String(cell.row.getValue("name"))}/events`;
        const text: string = cell.getValue();

        return formatLinkHandler(link, text);
      },
      header: t("organization.tabs.groups.newGroup.events.text"),
    },
  ];

  const dataset: IGroupData[] = data
    ? formatGroupData(data.organization.groups)
    : [];

  return (
    <React.StrictMode>
      <div>
        {_.isUndefined(data) || _.isEmpty(data) ? (
          <div />
        ) : (
          <div>
            <div>
              <Row>
                <Tables
                  columns={tableHeaders}
                  data={dataset}
                  extraButtons={
                    <Can do={"api_mutations_add_group_mutate"}>
                      <Tooltip
                        hide={runTour}
                        id={"organization.tabs.groups.newGroup.new.tooltip.btn"}
                        tip={t("organization.tabs.groups.newGroup.new.tooltip")}
                      >
                        <Button
                          id={"add-group"}
                          onClick={openNewGroupModal}
                          variant={"primary"}
                        >
                          <FontAwesomeIcon icon={faPlus} />
                          &nbsp;
                          {t("organization.tabs.groups.newGroup.new.text")}
                        </Button>
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
                      </Tooltip>
                    </Can>
                  }
                  id={"tblGroups"}
                />
              </Row>
            </div>
            {isGroupModalOpen ? (
              <AddGroupModal
                isOpen={true}
                onClose={closeNewGroupModal}
                organization={organizationName}
                runTour={enableTour}
              />
            ) : undefined}
          </div>
        )}
      </div>
    </React.StrictMode>
  );
};

export { OrganizationGroups };
