import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";

import { DataTableNext } from "components/DataTableNext/index";
import type {
  IFilterProps,
  IHeaderConfig,
} from "components/DataTableNext/types";
import { filterSearchText, filterText } from "components/DataTableNext/utils";
import type {
  IBillingData,
  IGetOrganizationBilling,
  IOrganizationBillingProps,
} from "scenes/Dashboard/containers/OrganizationBillingView/types";
import style from "scenes/Dashboard/containers/OrganizationGroupsView/index.css";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/OrganizationGroupsView/queries";
import { Col100, Row } from "styles/styledComponents";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IFilterSet {
  groupName: string;
  subscription: string;
}
const OrganizationBilling: React.FC<IOrganizationBillingProps> = (
  props: IOrganizationBillingProps
): JSX.Element => {
  const { organizationId } = props;

  // GraphQL operations
  const { data } = useQuery<IGetOrganizationBilling>(GET_ORGANIZATION_GROUPS, {
    onCompleted: (paramData: IGetOrganizationBilling): void => {
      if (_.isEmpty(paramData.organization.groups)) {
        Logger.warning("Empty groups", document.location.pathname);
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading organization groups", error);
      });
    },
    variables: {
      organizationId,
    },
  });

  // Auxiliary functions

  const formatGroupData: (groupData: IBillingData[]) => IBillingData[] = (
    groupData: IBillingData[]
  ): IBillingData[] =>
    groupData.map((group: IBillingData): IBillingData => {
      const name: string = group.name.toUpperCase();
      const subscription: string = _.capitalize(group.subscription);

      return {
        ...group,
        name,
        subscription,
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
        subscription: "",
      },
      localStorage
    );

  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  // Render Elements
  const tableHeaders: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "name",
      header: "Group Name",
    },
    {
      align: "center",
      dataField: "subscription",
      header: "Subscription",
    },
  ];

  const dataset: IBillingData[] = data
    ? formatGroupData(data.organization.groups)
    : [];

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchTextDataset: IBillingData[] = filterSearchText(
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
  const filterGroupNameDataset: IBillingData[] = filterText(
    dataset,
    filterOrganizationGroupsTable.groupName,
    "name"
  );

  function onSubscriptionChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    event.persist();
    setFilterOrganizationGroupsTable(
      (value): IFilterSet => ({
        ...value,
        subscription: event.target.value,
      })
    );
  }
  const filterSubscriptionDataset: IBillingData[] = filterText(
    dataset,
    filterOrganizationGroupsTable.subscription,
    "subscription"
  );

  function clearFilters(): void {
    setFilterOrganizationGroupsTable(
      (): IFilterSet => ({
        groupName: "",
        subscription: "",
      })
    );
    setSearchTextFilter("");
  }

  const resultDataset: IBillingData[] = _.intersection(
    filterSearchTextDataset,
    filterGroupNameDataset,
    filterSubscriptionDataset
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
      defaultValue: filterOrganizationGroupsTable.subscription,
      onChangeSelect: onSubscriptionChange,
      placeholder: "Subscription",
      selectOptions: {
        Continuous: "Continuous",
        Oneshot: "Oneshot",
      },
      tooltipId: "organization.tabs.groups.filtersTooltips.subscription.id",
      tooltipMessage: "organization.tabs.groups.filtersTooltips.subscription",
      type: "select",
    },
  ];

  return (
    <React.StrictMode>
      <div className={style.container}>
        <Row>
          <Col100>
            <Row>
              <DataTableNext
                bordered={true}
                clearFiltersButton={clearFilters}
                customFilters={{
                  customFiltersProps,
                  isCustomFilterEnabled,
                  onUpdateEnableCustomFilter: handleUpdateCustomFilter,
                  oneRowMessage: true,
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
                headers={tableHeaders}
                id={"tblGroups"}
                pageSize={10}
                search={false}
              />
            </Row>
          </Col100>
        </Row>
      </div>
    </React.StrictMode>
  );
};

export { OrganizationBilling };
