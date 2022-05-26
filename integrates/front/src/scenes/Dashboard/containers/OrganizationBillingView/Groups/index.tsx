import { useMutation } from "@apollo/client";
import { faMoneyBill } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { areMutationsValid } from "./helpers";
import { linkFormatter } from "./linkFormatter";
import { Container } from "./styles";
import type { IUpdateGroupResultAttr } from "./types";
import { UpdateSubscriptionModal } from "./UpdateSubscriptionModal";

import { UPDATE_GROUP_MUTATION } from "../queries";
import type { IGroupAttr } from "../types";
import { Button } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { tooltipFormatter } from "components/Table/headerFormatters/tooltipFormatter";
import { Table } from "components/Table/index";
import type { IFilterProps, IHeaderConfig } from "components/Table/types";
import { filterSearchText, filterText } from "components/Table/utils";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IFilterSet {
  forces: string;
  groupName: string;
  machine: string;
  service: string;
  squad: string;
  tier: string;
}

interface IOrganizationGroupsProps {
  billingPortal: string;
  groups: IGroupAttr[];
  onUpdate: () => void;
}

export const OrganizationGroups: React.FC<IOrganizationGroupsProps> = ({
  billingPortal,
  groups,
  onUpdate,
}: IOrganizationGroupsProps): JSX.Element => {
  const { t } = useTranslation();

  // States
  const defaultCurrentRow: IGroupAttr = {
    authors: {
      currentSpend: 0,
      total: 0,
    },
    forces: "",
    hasForces: false,
    hasMachine: false,
    hasSquad: false,
    machine: "",
    managed: false,
    name: "",
    permissions: [],
    service: "",
    squad: "",
    tier: "",
  };

  // Auxiliary functions
  const accesibleGroupsData = (groupData: IGroupAttr[]): IGroupAttr[] =>
    groupData.filter(
      (group): boolean =>
        (group.permissions.includes(
          "api_mutations_update_subscription_mutate"
        ) ||
          group.permissions.includes(
            "api_mutations_update_group_managed_mutate"
          )) &&
        group.authors !== null
    );

  const formatGroupsData = (groupData: IGroupAttr[]): IGroupAttr[] =>
    groupData.map((group: IGroupAttr): IGroupAttr => {
      const servicesParameters: Record<string, string> = {
        false: "organization.tabs.groups.disabled",
        true: "organization.tabs.groups.enabled",
      };
      const name: string = _.capitalize(group.name);
      const service: string = _.capitalize(group.service);
      const tier: string = _.capitalize(group.tier);
      const forces: string = t(servicesParameters[group.hasForces.toString()]);
      const machine: string = t(
        servicesParameters[group.hasMachine.toString()]
      );
      const squad: string = t(servicesParameters[group.hasSquad.toString()]);

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

  const [currentRow, setCurrentRow] = useState(defaultCurrentRow);
  const [isUpdatingSubscription, setIsUpdatingSubscription] = useState<
    false | { mode: "UPDATE" }
  >(false);
  const openUpdateModal = useCallback((groupRow?: Dictionary<string>): void => {
    if (groupRow) {
      setCurrentRow(groupRow as unknown as IGroupAttr);
      setIsUpdatingSubscription({ mode: "UPDATE" });
    }
  }, []);

  // Render Elements
  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "name",
      header: "Group Name",
      width: "20%",
    },
    {
      changeFunction: openUpdateModal,
      dataField: "managed",
      formatter: linkFormatter,
      header: "Managed",
      headerFormatter: tooltipFormatter,
      tooltipDataField: t("organization.tabs.billing.groups.managed.tooltip"),
      width: "10%",
    },
    {
      dataField: "tier",
      header: "Tier",
      width: "8%",
    },
    {
      dataField: "service",
      header: "Service",
      width: "9%",
    },
    {
      dataField: "machine",
      formatter: statusFormatter,
      header: "Machine",
      width: "9%",
    },
    {
      dataField: "squad",
      formatter: statusFormatter,
      header: "Squad",
      width: "8%",
    },
    {
      dataField: "forces",
      formatter: statusFormatter,
      header: "Forces",
      width: "8%",
    },
    {
      dataField: "authors.total",
      formatter: statusFormatter,
      header: "Authors",
      width: "9%",
    },
    {
      dataField: "authors.currentSpend",
      formatter: statusFormatter,
      header: "Month-to-date spend ($)",
      width: "19%",
    },
  ];

  const dataset: IGroupAttr[] = formatGroupsData(accesibleGroupsData(groups));

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchTextDataset: IGroupAttr[] = filterSearchText(
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
  const filterGroupNameDataset: IGroupAttr[] = filterText(
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
  const filterTierDataset: IGroupAttr[] = filterText(
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
  const filterServiceDataset: IGroupAttr[] = filterText(
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
  const filterMachineDataset: IGroupAttr[] = filterText(
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
  const filterSquadDataset: IGroupAttr[] = filterText(
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
  const filterForcesDataset: IGroupAttr[] = filterText(
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

  const resultDataset: IGroupAttr[] = _.intersection(
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

  // Edit group subscription
  const closeModal = useCallback((): void => {
    setIsUpdatingSubscription(false);
  }, []);
  const [updateGroup] = useMutation<IUpdateGroupResultAttr>(
    UPDATE_GROUP_MUTATION
  );
  const handleUpdateGroupSubmit = useCallback(
    async ({
      managed,
      subscription,
    }: {
      managed: string;
      subscription: string;
    }): Promise<void> => {
      const groupName = currentRow.name.toLowerCase();
      const updatedManaged: boolean = managed === "true";
      const isSubscriptionChanged: boolean =
        subscription !== currentRow.tier.toLocaleUpperCase();
      const isManagedChanged: boolean = updatedManaged !== currentRow.managed;

      try {
        const resultMutation = await updateGroup({
          variables: {
            comments: "",
            groupName,
            isManagedChanged,
            isSubscriptionChanged,
            managed: updatedManaged,
            subscription,
          },
        });
        if (areMutationsValid(resultMutation)) {
          onUpdate();
          closeModal();
          msgSuccess(
            t(
              "organization.tabs.billing.groups.updateSubscription.success.body"
            ),
            t(
              "organization.tabs.billing.groups.updateSubscription.success.title"
            )
          );
        }
      } catch (updateError: unknown) {
        switch (String(updateError).slice(7)) {
          case "Exception - Cannot perform action. Please add a valid payment method first":
            msgError(
              t(
                "organization.tabs.billing.groups.updateSubscription.errors.addPaymentMethod"
              )
            );
            break;
          case "Exception - Invalid subscription. Provided subscription is already active":
            msgError(
              t(
                "organization.tabs.billing.groups.updateSubscription.errors.alreadyActive"
              )
            );
            break;
          case "Exception - Invalid customer. Provided customer does not have a payment method":
            msgError(
              t(
                "organization.tabs.billing.groups.updateSubscription.errors.addPaymentMethod"
              )
            );
            break;
          case "Exception - Subscription could not be updated, please review your invoices":
            msgError(
              t(
                "organization.tabs.billing.groups.updateSubscription.errors.couldNotBeUpdated"
              )
            );
            break;
          case "Exception - Subscription could not be downgraded, payment intent for Squad failed":
            msgError(
              t(
                "organization.tabs.billing.groups.updateSubscription.errors.couldNotBeDowngraded"
              )
            );
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning("Couldn't update group subscription", updateError);
        }
      }
    },
    [
      closeModal,
      currentRow.managed,
      currentRow.name,
      currentRow.tier,
      onUpdate,
      t,
      updateGroup,
    ]
  );

  return (
    <Container>
      <Row>
        <div className={"w-100-ns"}>
          <Row>
            <h2>{t("organization.tabs.billing.groups.title")}</h2>
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
                <Can do={"api_resolvers_organization_billing_portal_resolve"}>
                  <ExternalLink href={billingPortal}>
                    <Button variant={"primary"}>
                      <FontAwesomeIcon icon={faMoneyBill} />
                      &nbsp;
                      {t("organization.tabs.billing.portal.title")}
                    </Button>
                  </ExternalLink>
                </Can>
              }
              headers={tableHeaders}
              id={"tblGroups"}
              pageSize={10}
              search={false}
            />
            {isUpdatingSubscription === false ? undefined : (
              <UpdateSubscriptionModal
                current={currentRow.tier.toUpperCase()}
                groupName={currentRow.name}
                managed={currentRow.managed}
                onClose={closeModal}
                onSubmit={handleUpdateGroupSubmit}
                permissions={currentRow.permissions}
              />
            )}
          </Row>
        </div>
      </Row>
    </Container>
  );
};
