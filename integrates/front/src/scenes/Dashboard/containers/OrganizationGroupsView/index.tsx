import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import { Button } from "components/Button";
import { Table } from "components/Table/index";
import type { IFilterProps, IHeaderConfig } from "components/Table/types";
import { filterSearchText, filterText } from "components/Table/utils";
import { TooltipWrapper } from "components/TooltipWrapper/index";
import { AddGroupModal } from "scenes/Dashboard/components/AddGroupModal";
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
import { translate } from "utils/translations/translate";

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

  // State management
  const [isGroupModalOpen, setGroupModalOpen] = useState(false);

  const openNewGroupModal: () => void = useCallback((): void => {
    setGroupModalOpen(true);
  }, []);

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
          msgError(translate.t("groupAlerts.errorTextsad"));
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

      return {
        ...group,
        description,
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
      header: translate.t("organization.tabs.groups.newGroup.name"),
    },
    {
      dataField: "description",
      header: translate.t("organization.tabs.groups.newGroup.description.text"),
    },
    { dataField: "plan", header: translate.t("organization.tabs.groups.plan") },
    {
      dataField: "userRole",
      formatter: (value: string): string =>
        translate.t(`userModal.roles.${_.camelCase(value)}`, {
          defaultValue: "-",
        }),
      header: translate.t("organization.tabs.groups.role"),
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
      placeholder: translate.t("organization.tabs.groups.plan"),
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
                            message={translate.t(
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
                              {translate.t(
                                "organization.tabs.groups.newGroup.new.text"
                              )}
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
