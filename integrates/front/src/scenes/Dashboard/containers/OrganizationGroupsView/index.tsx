import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import { Button } from "components/Button";
import { statusFormatter } from "components/DataTableNext/formatters";
import { DataTableNext } from "components/DataTableNext/index";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { TooltipWrapper } from "components/TooltipWrapper/index";
import { AddProjectModal } from "scenes/Dashboard/components/AddProjectModal";
import style from "scenes/Dashboard/containers/OrganizationGroupsView/index.css";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/OrganizationGroupsView/queries";
import type {
  IGetOrganizationGroups,
  IGroupData,
  IOrganizationGroupsProps,
} from "scenes/Dashboard/containers/OrganizationGroupsView/types";
import { ButtonToolbarCenter, Col100, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
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
  const [isProjectModalOpen, setProjectModalOpen] = useState(false);

  const openNewProjectModal: () => void = useCallback((): void => {
    setProjectModalOpen(true);
  }, []);

  // GraphQL operations
  const { data, refetch: refetchGroups } = useQuery(GET_ORGANIZATION_GROUPS, {
    onCompleted: (paramData: IGetOrganizationGroups): void => {
      if (_.isEmpty(paramData.organization.projects)) {
        Logger.warning("Empty projects", document.location.pathname);
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
  const closeNewProjectModal: () => void = useCallback((): void => {
    setProjectModalOpen(false);
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
    groupData.map(
      (group: IGroupData): IGroupData => {
        const servicesParameters: Record<string, string> = {
          false: "organization.tabs.groups.disabled",
          true: "organization.tabs.groups.enabled",
        };
        const name: string = group.name.toUpperCase();
        const description: string = _.capitalize(group.description);
        const subscription: string = _.capitalize(group.subscription);
        const drills: string = translate.t(
          servicesParameters[group.hasDrills.toString()]
        );
        const forces: string = translate.t(
          servicesParameters[group.hasForces.toString()]
        );
        const integrates: string = translate.t(
          servicesParameters[group.hasIntegrates.toString()]
        );

        return {
          ...group,
          description,
          drills,
          forces,
          integrates,
          name,
          subscription,
        };
      }
    );

  // Render Elements
  const tableHeaders: IHeaderConfig[] = [
    { align: "center", dataField: "name", header: "Group Name" },
    { align: "center", dataField: "description", header: "Description" },
    { align: "center", dataField: "subscription", header: "Service Type" },
    {
      align: "center",
      dataField: "integrates",
      formatter: statusFormatter,
      header: "Integrates",
    },
    {
      align: "center",
      dataField: "drills",
      formatter: statusFormatter,
      header: "Drills",
    },
    {
      align: "center",
      dataField: "forces",
      formatter: statusFormatter,
      header: "Forces",
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
          <Can do={"backend_api_mutations_create_group_mutate"}>
            <ButtonToolbarCenter>
              <TooltipWrapper
                id={"organization.tabs.groups.newGroup.new.tooltip.btn"}
                message={translate.t(
                  "organization.tabs.groups.newGroup.new.tooltip"
                )}
              >
                <Button id={"add-group"} onClick={openNewProjectModal}>
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
              {/* eslint-disable-next-line react/forbid-component-props */}
              <Row>
                <DataTableNext
                  bordered={true}
                  dataset={formatGroupData(data.organization.projects)}
                  defaultSorted={{ dataField: "name", order: "asc" }}
                  exportCsv={false}
                  headers={tableHeaders}
                  id={"tblGroups"}
                  pageSize={15}
                  rowEvents={{ onClick: handleRowClick }}
                  search={true}
                />
              </Row>
            </Col100>
            {isProjectModalOpen ? (
              <AddProjectModal
                isOpen={true}
                onClose={closeNewProjectModal}
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
