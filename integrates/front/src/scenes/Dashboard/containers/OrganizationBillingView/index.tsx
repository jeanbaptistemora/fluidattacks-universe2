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
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
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
  machine: string;
  service: string;
  squad: string;
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
      const servicesParameters: Record<string, string> = {
        false: "organization.tabs.groups.disabled",
        true: "organization.tabs.groups.enabled",
      };
      const name: string = group.name.toUpperCase();
      const service: string = _.capitalize(group.service);
      const subscription: string = _.capitalize(group.subscription);
      const machine: string = translate.t(
        servicesParameters[group.hasMachine.toString()]
      );
      const squad: string = translate.t(
        servicesParameters[group.hasSquad.toString()]
      );

      return {
        ...group,
        machine,
        name,
        service,
        squad,
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
        machine: "",
        service: "",
        squad: "",
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
    {
      align: "center",
      dataField: "service",
      header: "Service",
    },
    {
      align: "left",
      dataField: "machine",
      formatter: pointStatusFormatter,
      header: "Machine",
      width: "90px",
    },
    {
      align: "left",
      dataField: "squad",
      formatter: pointStatusFormatter,
      header: "Squad",
      width: "90px",
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

  function onServiceChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterOrganizationGroupsTable(
      (value): IFilterSet => ({
        ...value,
        service: event.target.value,
      })
    );
  }
  const filterServiceDataset: IBillingData[] = filterText(
    dataset,
    filterOrganizationGroupsTable.service,
    "service"
  );

  function onMachineChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterOrganizationGroupsTable(
      (value): IFilterSet => ({
        ...value,
        machine: event.target.value,
      })
    );
  }
  const filterMachineDataset: IBillingData[] = filterText(
    dataset,
    filterOrganizationGroupsTable.machine,
    "machine"
  );

  function onSquadChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterOrganizationGroupsTable(
      (value): IFilterSet => ({
        ...value,
        squad: event.target.value,
      })
    );
  }
  const filterSquadDataset: IBillingData[] = filterText(
    dataset,
    filterOrganizationGroupsTable.squad,
    "squad"
  );

  function clearFilters(): void {
    setFilterOrganizationGroupsTable(
      (): IFilterSet => ({
        groupName: "",
        machine: "",
        service: "",
        squad: "",
        subscription: "",
      })
    );
    setSearchTextFilter("");
  }

  const resultDataset: IBillingData[] = _.intersection(
    filterSearchTextDataset,
    filterGroupNameDataset,
    filterSubscriptionDataset,
    filterServiceDataset,
    filterMachineDataset,
    filterSquadDataset
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
    {
      defaultValue: filterOrganizationGroupsTable.service,
      onChangeSelect: onServiceChange,
      placeholder: "Service",
      selectOptions: {
        Black: "Black",
        White: "White",
      },
      tooltipId: "organization.tabs.groups.filtersTooltips.service.id",
      tooltipMessage: "organization.tabs.groups.filtersTooltips.service",
      type: "select",
    },
    {
      defaultValue: filterOrganizationGroupsTable.machine,
      onChangeSelect: onMachineChange,
      placeholder: "Machine",
      selectOptions: {
        Disabled: "Disabled",
        Enabled: "Enabled",
      },
      tooltipId: "organization.tabs.groups.filtersTooltips.machine.id",
      tooltipMessage: "organization.tabs.groups.filtersTooltips.machine",
      type: "select",
    },
    {
      defaultValue: filterOrganizationGroupsTable.squad,
      onChangeSelect: onSquadChange,
      placeholder: "Squad",
      selectOptions: {
        Disabled: "Disabled",
        Enabled: "Enabled",
      },
      tooltipId: "organization.tabs.groups.filtersTooltips.squad.id",
      tooltipMessage: "organization.tabs.groups.filtersTooltips.squad",
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
                id={"tblBilling"}
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
