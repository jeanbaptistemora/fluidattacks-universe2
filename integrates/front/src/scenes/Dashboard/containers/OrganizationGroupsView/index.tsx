import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import type { TableColumnFilterProps } from "react-bootstrap-table-next";
import { selectFilter, textFilter } from "react-bootstrap-table2-filter";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import {
  selectOptionsMachine,
  selectOptionsService,
  selectOptionsSquad,
  selectOptionsSubscription,
} from "./filters";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext/index";
import type { IHeaderConfig } from "components/DataTableNext/types";
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

  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>(
    "organizationGroupsFilters",
    false
  );

  const handleUpdateFilter: () => void = useCallback((): void => {
    setFilterEnabled(!isFilterEnabled);
  }, [isFilterEnabled, setFilterEnabled]);

  const onFilterGroupName: TableColumnFilterProps["onFilter"] = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("groupNameFilter", filterVal);
  };
  const onFilterSubscription: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("subscriptionFilter", filterVal);
  };
  const onFilterService: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("serviceFilter", filterVal);
  };
  const onFilterMachine: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("machineFilter", filterVal);
  };
  const onFilterSquad: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("squadFilter", filterVal);
  };

  // Render Elements
  const tableHeaders: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "name",
      filter: textFilter({
        defaultValue: _.get(sessionStorage, "groupNameFilter"),
        delay: 1000,
        onFilter: onFilterGroupName,
      }),
      header: "Group Name",
    },
    { align: "center", dataField: "description", header: "Description" },
    {
      align: "center",
      dataField: "subscription",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "subscriptionFilter"),
        onFilter: onFilterSubscription,
        options: selectOptionsSubscription,
        placeholder: "ALL",
      }),
      header: "Subscription",
    },
    {
      align: "center",
      dataField: "service",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "serviceFilter"),
        onFilter: onFilterService,
        options: selectOptionsService,
        placeholder: "ALL",
      }),
      header: "Service",
    },
    {
      align: "left",
      dataField: "machine",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "machineFilter"),
        onFilter: onFilterMachine,
        options: selectOptionsMachine,
        placeholder: "ALL",
      }),
      formatter: pointStatusFormatter,
      header: "Machine",
      width: "90px",
    },
    {
      align: "left",
      dataField: "squad",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "squadFilter"),
        onFilter: onFilterSquad,
        options: selectOptionsSquad,
        placeholder: "ALL",
      }),
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
                  dataset={formatGroupData(data.organization.groups)}
                  defaultSorted={{ dataField: "name", order: "asc" }}
                  exportCsv={false}
                  headers={tableHeaders}
                  id={"tblGroups"}
                  isFilterEnabled={isFilterEnabled}
                  onUpdateEnableFilter={handleUpdateFilter}
                  pageSize={10}
                  rowEvents={{ onClick: handleRowClick }}
                  search={true}
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
