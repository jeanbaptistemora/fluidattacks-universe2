import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import { Button } from "components/Button";
import { tooltipFormatter } from "components/Table/headerFormatters/tooltipFormatter";
import { Table } from "components/Table/index";
import type { IFilterProps, IHeaderConfig } from "components/Table/types";
import { filterSearchText, filterText } from "components/Table/utils";
import { TooltipWrapper } from "components/TooltipWrapper/index";
import { Tour } from "components/Tour/index";
import { AddGroupModal } from "scenes/Dashboard/components/AddGroupModal";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/OrganizationGroupsView/queries";
import type {
  IGetOrganizationGroups,
  IGroupData,
  IOrganizationGroupsProps,
} from "scenes/Dashboard/containers/OrganizationGroupsView/types";
import { ButtonToolbar, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface IFilterSet {
  groupName: string;
  plan: string;
}

const OrganizationGroups: React.FC<IOrganizationGroupsProps> = (
  props: IOrganizationGroupsProps
): JSX.Element => {
  const { organizationId } = props;
  const { organizationName } = useParams<{ organizationName: string }>();
  const { url } = useRouteMatch();
  const { push } = useHistory();
  const { t } = useTranslation();

  // State management
  const [isGroupModalOpen, setGroupModalOpen] = useState(false);
  const [runTour, toggleTour] = useState(false);

  const openNewGroupModal: () => void = useCallback((): void => {
    if (runTour) {
      toggleTour(false);
    }
    setGroupModalOpen(true);
  }, [runTour, toggleTour]);

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
    setGroupModalOpen(false);
    void refetchGroups();
  }, [refetchGroups]);
  // Auxiliary functions
  const goToGroup: (groupName: string) => void = (groupName: string): void => {
    push(`${url}/${groupName.toLowerCase()}/vulns`);
  };

  const handleRowClick: (
    event: React.FormEvent<HTMLButtonElement>,
    rowInfo: { name: string }
  ) => void = (
    _0: React.FormEvent<HTMLButtonElement>,
    rowInfo: { name: string }
  ): void => {
    goToGroup(rowInfo.name);
  };

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
          ? "Ok"
          : group.events.filter((event): boolean =>
              event.eventStatus.includes("CREATED")
            ).length > 0
          ? "Failed"
          : "Ok";

      return {
        ...group,
        description,
        eventFormat,
        name,
        plan,
      };
    });

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("organizationGroupsCustomFilters", false);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [filterOrganizationGroupsTable, setFilterOrganizationGroupsTable] =
    useStoredState(
      "filterOrganizationGroupset",
      {
        groupName: "",
        plan: "",
      },
      localStorage
    );

  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "name",
      header: t("organization.tabs.groups.newGroup.name"),
    },
    {
      dataField: "description",
      header: t("organization.tabs.groups.newGroup.description.text"),
    },
    { dataField: "plan", header: t("organization.tabs.groups.plan") },
    {
      dataField: "userRole",
      formatter: (value: string): string =>
        t(`userModal.roles.${_.camelCase(value)}`, {
          defaultValue: "-",
        }),
      header: t("organization.tabs.groups.role"),
    },
    {
      dataField: "eventFormat",
      formatter: statusFormatter,
      header: t("organization.tabs.groups.newGroup.status.text"),
      headerFormatter: tooltipFormatter,
      tooltipDataField: t("organization.tabs.groups.newGroup.status.tooltip"),
      wrapped: true,
    },
  ];

  const dataset: IGroupData[] = data
    ? formatGroupData(data.organization.groups)
    : [];

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchTextDataset: IGroupData[] = filterSearchText(
    dataset,
    searchTextFilter
  );

  function onGroupNameChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterOrganizationGroupsTable(
      (value): IFilterSet => ({
        ...value,
        groupName: event.target.value,
      })
    );
  }
  const filterGroupNameDataset: IGroupData[] = filterText(
    dataset,
    filterOrganizationGroupsTable.groupName,
    "name"
  );

  function onPlanChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterOrganizationGroupsTable(
      (value): IFilterSet => ({
        ...value,
        plan: event.target.value,
      })
    );
  }

  const filterPlanDataset: IGroupData[] = filterText(
    dataset,
    filterOrganizationGroupsTable.plan,
    "plan"
  );
  function clearFilters(): void {
    setFilterOrganizationGroupsTable(
      (): IFilterSet => ({
        groupName: "",
        plan: "",
      })
    );
    setSearchTextFilter("");
  }

  const resultDataset: IGroupData[] = _.intersection(
    filterSearchTextDataset,
    filterGroupNameDataset,
    filterPlanDataset
  );

  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: filterOrganizationGroupsTable.groupName,
      onChangeInput: onGroupNameChange,
      placeholder: "Group Name",
      tooltipId: "organization.tabs.groups.filtersTooltips.groupName.id",
      tooltipMessage: "organization.tabs.groups.filtersTooltips.groupName",
      type: "text",
    },
    {
      defaultValue: filterOrganizationGroupsTable.plan,
      onChangeSelect: onPlanChange,
      placeholder: t("organization.tabs.groups.plan"),
      selectOptions: {
        Machine: "Machine",
        Oneshot: "Oneshot",
        Squad: "Squad",
      },
      tooltipId: "organization.tabs.groups.filtersTooltips.plan.id",
      tooltipMessage: "organization.tabs.groups.filtersTooltips.plan",
      type: "select",
    },
  ];

  return (
    <React.StrictMode>
      <div>
        {_.isUndefined(data) || _.isEmpty(data) ? (
          <div />
        ) : (
          <div>
            <div>
              <Row>
                <Table
                  clearFiltersButton={clearFilters}
                  customFilters={{
                    customFiltersProps,
                    isCustomFilterEnabled,
                    onUpdateEnableCustomFilter: handleUpdateCustomFilter,
                    resultSize: {
                      current: resultDataset.length,
                      total: dataset.length,
                    },
                  }}
                  customSearch={{
                    customSearchDefault: searchTextFilter,
                    isCustomSearchEnabled: true,
                    onUpdateCustomSearch: onSearchTextChange,
                    position: "right",
                  }}
                  dataset={resultDataset}
                  defaultSorted={{ dataField: "name", order: "asc" }}
                  exportCsv={false}
                  extraButtons={
                    <Row>
                      <Can do={"api_mutations_add_group_mutate"}>
                        <ButtonToolbar>
                          <TooltipWrapper
                            id={
                              "organization.tabs.groups.newGroup.new.tooltip.btn"
                            }
                            message={t(
                              "organization.tabs.groups.newGroup.new.tooltip"
                            )}
                          >
                            <Button
                              id={"add-group"}
                              onClick={openNewGroupModal}
                              variant={"primary"}
                            >
                              <FontAwesomeIcon icon={faPlus} />
                              &nbsp;
                              {t("organization.tabs.groups.newGroup.new.text")}
                              {runTour ? (
                                <Tour
                                  run={true}
                                  steps={[
                                    {
                                      content: t("tours.addGroup.addButton"),
                                      disableBeacon: true,
                                      // HideCloseButton: true,
                                      hideFooter: true,
                                      target: "#add-group",
                                    },
                                  ]}
                                />
                              ) : undefined}
                            </Button>
                          </TooltipWrapper>
                        </ButtonToolbar>
                      </Can>
                    </Row>
                  }
                  headers={tableHeaders}
                  id={"tblGroups"}
                  pageSize={10}
                  rowEvents={{ onClick: handleRowClick }}
                  search={false}
                />
              </Row>
            </div>
            {isGroupModalOpen ? (
              <AddGroupModal
                isOpen={true}
                onClose={closeNewGroupModal}
                organization={organizationName}
              />
            ) : undefined}
          </div>
        )}
      </div>
    </React.StrictMode>
  );
};

export { OrganizationGroups };
