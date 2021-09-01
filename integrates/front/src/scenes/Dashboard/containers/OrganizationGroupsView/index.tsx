import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext/index";
import type {
  IFilterProps,
  IHeaderConfig,
} from "components/DataTableNext/types";
import { filterSearchText, filterText } from "components/DataTableNext/utils";
import { TooltipWrapper } from "components/TooltipWrapper/index";
import { AddGroupModal } from "scenes/Dashboard/components/AddGroupModal";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import style from "scenes/Dashboard/containers/OrganizationGroupsView/index.css";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/OrganizationGroupsView/queries";
import type {
  IGetOrganizationGroups,
  IGroupData,
  IOrganizationGroupsProps,
} from "scenes/Dashboard/containers/OrganizationGroupsView/types";
import { ButtonToolbarCenter, Col100, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

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
  const { data, refetch: refetchGroups } = useQuery(GET_ORGANIZATION_GROUPS, {
    onCompleted: (paramData: IGetOrganizationGroups): void => {
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
      const servicesParameters: Record<string, string> = {
        false: "organization.tabs.groups.disabled",
        true: "organization.tabs.groups.enabled",
      };
      const name: string = group.name.toUpperCase();
      const description: string = _.capitalize(group.description);
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
        description,
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
  const [groupNameFilter, setGroupNameFilter] = useState("");
  const [subscriptionFilter, setSubscriptionFilter] = useState("");
  const [serviceFilter, setServiceFilter] = useState("");
  const [machineFilter, setMachineFilter] = useState("");
  const [squadFilter, setSquadFilter] = useState("");

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
    { align: "center", dataField: "description", header: "Description" },
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
    {
      align: "center",
      dataField: "userRole",
      formatter: (value: string): string =>
        translate.t(`userModal.roles.${_.camelCase(value)}`, {
          defaultValue: "-",
        }),
      header: "Role",
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
    setGroupNameFilter(event.target.value);
  }
  const filterGroupNameDataset: IGroupData[] = filterText(
    dataset,
    groupNameFilter,
    "name"
  );

  function onSubscriptionChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setSubscriptionFilter(event.target.value);
  }
  const filterSubscriptionDataset: IGroupData[] = filterText(
    dataset,
    subscriptionFilter,
    "subscription"
  );

  function onServiceChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    setServiceFilter(event.target.value);
  }
  const filterServiceDataset: IGroupData[] = filterText(
    dataset,
    serviceFilter,
    "service"
  );

  function onMachineChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    setMachineFilter(event.target.value);
  }
  const filterMachineDataset: IGroupData[] = filterText(
    dataset,
    machineFilter,
    "machine"
  );

  function onSquadChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    setSquadFilter(event.target.value);
  }
  const filterSquadDataset: IGroupData[] = filterText(
    dataset,
    squadFilter,
    "squad"
  );

  const resultDataset: IGroupData[] = _.intersection(
    filterSearchTextDataset,
    filterGroupNameDataset,
    filterSubscriptionDataset,
    filterServiceDataset,
    filterMachineDataset,
    filterSquadDataset
  );

  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: groupNameFilter,
      onChangeInput: onGroupNameChange,
      placeholder: "Group Name",
      tooltipId: "organization.tabs.groups.filtersTooltips.groupName.id",
      tooltipMessage: "organization.tabs.groups.filtersTooltips.groupName",
      type: "text",
    },
    {
      defaultValue: subscriptionFilter,
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
      defaultValue: serviceFilter,
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
      defaultValue: machineFilter,
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
      defaultValue: squadFilter,
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
          <Can do={"api_mutations_add_group_mutate"}>
            <ButtonToolbarCenter>
              <TooltipWrapper
                id={"organization.tabs.groups.newGroup.new.tooltip.btn"}
                message={translate.t(
                  "organization.tabs.groups.newGroup.new.tooltip"
                )}
              >
                <Button id={"add-group"} onClick={openNewGroupModal}>
                  <FontAwesomeIcon icon={faPlus} />
                  &nbsp;
                  {translate.t("organization.tabs.groups.newGroup.new.text")}
                </Button>
              </TooltipWrapper>
            </ButtonToolbarCenter>
          </Can>
        </Row>
        {_.isUndefined(data) || _.isEmpty(data) ? (
          <div />
        ) : (
          <Row>
            <Col100>
              <Row>
                <DataTableNext
                  bordered={true}
                  customFilters={{
                    customFiltersProps,
                    isCustomFilterEnabled,
                    onUpdateEnableCustomFilter: handleUpdateCustomFilter,
                  }}
                  customSearch={{
                    customSearchDefault: searchTextFilter,
                    isCustomSearchEnabled: true,
                    onUpdateCustomSearch: onSearchTextChange,
                  }}
                  dataset={resultDataset}
                  defaultSorted={{ dataField: "name", order: "asc" }}
                  exportCsv={false}
                  headers={tableHeaders}
                  id={"tblGroups"}
                  pageSize={10}
                  rowEvents={{ onClick: handleRowClick }}
                  search={false}
                />
              </Row>
            </Col100>
            {isGroupModalOpen ? (
              <AddGroupModal
                isOpen={true}
                onClose={closeNewGroupModal}
                organization={organizationName}
              />
            ) : undefined}
          </Row>
        )}
      </div>
    </React.StrictMode>
  );
};

export { OrganizationGroups };
