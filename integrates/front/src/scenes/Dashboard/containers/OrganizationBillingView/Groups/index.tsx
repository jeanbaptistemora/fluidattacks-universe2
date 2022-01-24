import _ from "lodash";
import React, { useCallback, useState } from "react";

import { Container } from "./styles";

import type { IGroupAttr } from "../types";
import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext/index";
import type {
  IFilterProps,
  IHeaderConfig,
} from "components/DataTableNext/types";
import { filterSearchText, filterText } from "components/DataTableNext/utils";
import { Modal } from "components/Modal";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { useStoredState } from "utils/hooks";
import { translate } from "utils/translations/translate";

interface IFilterSet {
  forces: string;
  groupName: string;
  machine: string;
  service: string;
  squad: string;
  tier: string;
}

interface IOrganizationBillingGroupsProps {
  groups: IGroupAttr[];
}

export const OrganizationBillingGroups: React.FC<IOrganizationBillingGroupsProps> =
  ({ groups }: IOrganizationBillingGroupsProps): JSX.Element => {
    // States
    const defaultCurrentRow: IGroupAttr = {
      forces: "",
      hasForces: false,
      hasMachine: false,
      hasSquad: false,
      machine: "",
      name: "",
      service: "",
      squad: "",
      tier: "",
    };

    const [currentRow, updateRow] = useState(defaultCurrentRow);
    const [isBillingDetailsModalOpen, setBillingDetailsModalOpen] =
      useState(false);

    // Auxiliary functions

    const formatGroupData: (groupData: IGroupAttr[]) => IGroupAttr[] = (
      groupData: IGroupAttr[]
    ): IGroupAttr[] =>
      groupData.map((group: IGroupAttr): IGroupAttr => {
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

    const dataset: IGroupAttr[] = formatGroupData(groups);

    function onSearchTextChange(
      event: React.ChangeEvent<HTMLInputElement>
    ): void {
      setSearchTextFilter(event.target.value);
    }
    const filterSearchTextDataset: IGroupAttr[] = filterSearchText(
      dataset,
      searchTextFilter
    );

    function onGroupNameChange(
      event: React.ChangeEvent<HTMLInputElement>
    ): void {
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

    function onServiceChange(
      event: React.ChangeEvent<HTMLSelectElement>
    ): void {
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

    function onMachineChange(
      event: React.ChangeEvent<HTMLSelectElement>
    ): void {
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

    const openSeeBillingDetailsModal: (
      event: Record<string, unknown>,
      row: IGroupAttr
    ) => void = (_0: Record<string, unknown>, row: IGroupAttr): void => {
      updateRow(row);
      setBillingDetailsModalOpen(true);
    };

    const closeSeeBillingDetailsModal: () => void = useCallback((): void => {
      setBillingDetailsModalOpen(false);
    }, []);

    return (
      <Container>
        <Row>
          <Col100>
            <Row>
              <h2>{translate.t("organization.tabs.billing.groups.title")}</h2>
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
                id={"tblBillingGroups"}
                pageSize={10}
                rowEvents={{ onClick: openSeeBillingDetailsModal }}
                search={false}
              />
              <Modal
                headerTitle={translate.t(
                  "organization.tabs.billing.modal.title"
                )}
                onEsc={closeSeeBillingDetailsModal}
                open={isBillingDetailsModalOpen}
                size={"largeModal"}
              >
                <div>{currentRow.name}</div>
                <Row>
                  <Col100>
                    <ButtonToolbar>
                      <Button onClick={closeSeeBillingDetailsModal}>
                        {translate.t(
                          "organization.tabs.billing.modal.continue"
                        )}
                      </Button>
                      <Button onClick={closeSeeBillingDetailsModal}>
                        {translate.t("organization.tabs.billing.modal.close")}
                      </Button>
                    </ButtonToolbar>
                  </Col100>
                </Row>
              </Modal>
            </Row>
          </Col100>
        </Row>
      </Container>
    );
  };
