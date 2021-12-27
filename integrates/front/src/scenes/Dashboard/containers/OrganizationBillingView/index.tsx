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
import { GET_ORGANIZATION_BILLING } from "scenes/Dashboard/containers/OrganizationBillingView/queries";
import type {
  IBillingData,
  IGetOrganizationBilling,
  IOrganizationBillingProps,
} from "scenes/Dashboard/containers/OrganizationBillingView/types";
import style from "scenes/Dashboard/containers/OrganizationGroupsView/index.css";
import { Col100, Row } from "styles/styledComponents";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IFilterSet {
  forces: string;
  groupName: string;
  machine: string;
  service: string;
  squad: string;
  tier: string;
}
const OrganizationBilling: React.FC<IOrganizationBillingProps> = (
  props: IOrganizationBillingProps
): JSX.Element => {
  const { organizationId } = props;

  // GraphQL operations
  const { data } = useQuery<IGetOrganizationBilling>(GET_ORGANIZATION_BILLING, {
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
      const tier: string = _.capitalize(group.tier);
      const forces: string = translate.t(
        servicesParameters[group.hasForces.toString()]
      );
      const machine: string = translate.t(
        servicesParameters[group.hasMachine.toString()]
      );
      const squad: string = translate.t(
        servicesParameters[group.hasSquad.toString()]
      );

      return {
        ...group,
        forces,
        machine,
        name,
        service,
        squad,
        tier,
      };
    });

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("organizationGroupsCustomFilters", false);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [filterOrganizationGroupsTable, setFilterOrganizationGroupsTable] =
    useStoredState(
      "filterOrganizationGroupset",
      {
        forces: "",
        groupName: "",
        machine: "",
        service: "",
        squad: "",
        tier: "",
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
      dataField: "tier",
      header: "Tier",
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
    {
      align: "left",
      dataField: "forces",
      formatter: pointStatusFormatter,
      header: "Forces",
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

  function onTierChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterOrganizationGroupsTable(
      (value): IFilterSet => ({
        ...value,
        tier: event.target.value,
      })
    );
  }
  const filterTierDataset: IBillingData[] = filterText(
    dataset,
    filterOrganizationGroupsTable.tier,
    "tier"
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

  function onForcesChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterOrganizationGroupsTable(
      (value): IFilterSet => ({
        ...value,
        forces: event.target.value,
      })
    );
  }
  const filterForcesDataset: IBillingData[] = filterText(
    dataset,
    filterOrganizationGroupsTable.forces,
    "forces"
  );

  function clearFilters(): void {
    setFilterOrganizationGroupsTable(
      (): IFilterSet => ({
        forces: "",
        groupName: "",
        machine: "",
        service: "",
        squad: "",
        tier: "",
      })
    );
    setSearchTextFilter("");
  }

  const resultDataset: IBillingData[] = _.intersection(
    filterSearchTextDataset,
    filterGroupNameDataset,
    filterTierDataset,
    filterServiceDataset,
    filterMachineDataset,
    filterSquadDataset,
    filterForcesDataset
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
      defaultValue: filterOrganizationGroupsTable.tier,
      onChangeSelect: onTierChange,
      placeholder: "Tier",
      selectOptions: {
        Disabled: "Disabled",
        Enabled: "Enabled",
      },
      tooltipId: "organization.tabs.groups.filtersTooltips.tier.id",
      tooltipMessage: "organization.tabs.groups.filtersTooltips.tier",
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
    {
      defaultValue: filterOrganizationGroupsTable.forces,
      onChangeSelect: onForcesChange,
      placeholder: "Forces",
      selectOptions: {
        Disabled: "Disabled",
        Enabled: "Enabled",
      },
      tooltipId: "organization.tabs.groups.filtersTooltips.forces.id",
      tooltipMessage: "organization.tabs.groups.filtersTooltips.forces",
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
