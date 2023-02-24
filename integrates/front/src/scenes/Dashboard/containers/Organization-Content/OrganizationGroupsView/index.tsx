import { useQuery } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ColumnDef } from "@tanstack/react-table";
import _ from "lodash";
import React, { StrictMode, useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { formatGroupData, getTrialTip } from "./utils";

import { Button } from "components/Button";
import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Table } from "components/Table";
import { formatLinkHandler } from "components/Table/formatters/linkFormatter";
import { BaseStep, Tour } from "components/Tour/index";
import { AddGroupModal } from "scenes/Dashboard/components/AddGroupModal";
import { OrganizationGroupOverview } from "scenes/Dashboard/containers/Organization-Content/OrganizationGroupsView/overview";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/Organization-Content/OrganizationGroupsView/queries";
import type {
  IGetOrganizationGroups,
  IGroupData,
  IOrganizationGroupsProps,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationGroupsView/types";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const OrganizationGroups: React.FC<IOrganizationGroupsProps> = (
  props
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
      onCompleted: (paramData): void => {
        if (_.isEmpty(paramData.organization.groups)) {
          Logger.warning("Empty groups", document.location.pathname);
        }
      },
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
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
  const closeNewGroupModal = useCallback((): void => {
    if (enableTour) {
      user.setUser({
        tours: {
          newGroup: true,
          newRiskExposure: user.tours.newRiskExposure,
          newRoot: user.tours.newRoot,
          welcome: user.tours.welcome,
        },
        userEmail: user.userEmail,
        userIntPhone: user.userIntPhone,
        userName: user.userName,
      });
    }
    setIsGroupModalOpen(false);
    void refetchGroups();
  }, [enableTour, refetchGroups, user]);

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
      accessorKey: "status",
      cell: (cell): JSX.Element => {
        const link = `groups/${String(cell.row.getValue("name"))}/scope`;
        const text = cell.getValue<string>();
        const showTrialTip =
          text === t(`organization.tabs.groups.status.trial`);
        const showSuspendedTip =
          text === t(`organization.tabs.groups.status.underReview`);
        const infoTip = showTrialTip
          ? getTrialTip(data?.organization.trial)
          : t(`organization.tabs.groups.status.underReviewTip`);

        return formatLinkHandler(
          link,
          text,
          showTrialTip || showSuspendedTip,
          infoTip
        );
      },
      header: t("organization.tabs.groups.status.header"),
    },
    {
      accessorKey: "plan",
      header: t("organization.tabs.groups.plan"),
    },
    {
      accessorKey: "vulnerabilities",
      cell: (cell): JSX.Element => {
        const link = `groups/${String(cell.row.getValue("name"))}/vulns`;
        const text = cell.getValue<string>();

        return formatLinkHandler(link, text);
      },
      header: t("organization.tabs.groups.vulnerabilities.header"),
    },
    {
      accessorKey: "description",
      header: t("organization.tabs.groups.newGroup.description.text"),
    },
    {
      accessorKey: "userRole",
      cell: (cell): string => {
        return t(`userModal.roles.${_.camelCase(cell.getValue())}`, {
          defaultValue: "-",
        });
      },
      header: t("organization.tabs.groups.role"),
    },
    {
      accessorKey: "eventFormat",
      cell: (cell): JSX.Element => {
        const link = `groups/${String(cell.row.getValue("name"))}/events`;
        const text = cell.getValue<string>();

        return formatLinkHandler(link, text);
      },
      header: t("organization.tabs.groups.newGroup.events.text"),
    },
  ];

  const dataset = data ? formatGroupData(data.organization.groups) : [];

  const [filters, setFilters] = useState<IFilter<IGroupData>[]>([
    {
      filterFn: "includesInsensitive",
      id: "name",
      key: "name",
      label: t("organization.tabs.groups.newGroup.name"),
      type: "text",
    },
    {
      id: "plan",
      key: "plan",
      label: t("organization.tabs.groups.plan"),
      selectOptions: ["Machine", "Oneshot", "Squad"],
      type: "select",
    },
  ]);

  const filteredDataset = useFilters(dataset, filters);

  return (
    <StrictMode>
      {_.isUndefined(data) || _.isEmpty(data) ? undefined : (
        <React.Fragment>
          <OrganizationGroupOverview
            coveredAuthors={data.organization.coveredAuthors}
            coveredRepositories={data.organization.coveredRepositories}
            missedAuthors={data.organization.missedAuthors}
            missedRepositories={data.organization.missedRepositories}
            organizationName={data.organization.name}
          />
          <br />
          <Table
            columns={tableHeaders}
            data={filteredDataset}
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
            filters={<Filters filters={filters} setFilters={setFilters} />}
            id={"tblGroups"}
          />
        </React.Fragment>
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
