import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import {
  ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";
import { Button } from "../../../../components/Button";
import { statusFormatter } from "../../../../components/DataTableNext/formatters";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeaderConfig } from "../../../../components/DataTableNext/types";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import { Can } from "../../../../utils/authz/Can";
import Logger from "../../../../utils/logger";
import { msgError } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { AddProjectModal } from "../../components/AddProjectModal";
import { default as style } from "./index.css";
import { GET_ORGANIZATION_GROUPS } from "./queries";
import { IGroupData, IOrganizationGroupsProps } from "./types";

const organizationGroups: React.FC<IOrganizationGroupsProps> = (props: IOrganizationGroupsProps): JSX.Element => {
  const { organizationId } = props;
  const { organizationName } = useParams();
  const { url } = useRouteMatch();
  const { push } = useHistory();

  // State management
  const [isProjectModalOpen, setProjectModalOpen] = React.useState(false);

  const openNewProjectModal: (() => void) = (): void => {
    setProjectModalOpen(true);
  };
  const closeNewProjectModal: (() => void) = (): void => {
    setProjectModalOpen(false);
    refetchGroups();
  };

  // GraphQL operations
  const { data, refetch: refetchGroups } = useQuery(GET_ORGANIZATION_GROUPS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred loading organization groups", error);
      });
    },
    variables: {
      organizationId,
    },
  });

  // Auxiliary functions
  const goToGroup: ((groupName: string) => void) = (groupName: string): void => {
    push(`${url}/${groupName.toLowerCase()}/`);
  };

  const handleRowClick: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string }) => void) = (
    _0: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string },
  ): void => {
    goToGroup(rowInfo.name);
  };

  const formatGroupData: (groupData: IGroupData[]) => IGroupData[] =
      (groupData: IGroupData[]): IGroupData[] => groupData.map((group: IGroupData) => {
    const servicesParameters: { [key: string]: string } = {
      false: "organization.tabs.groups.disabled",
      true: "organization.tabs.groups.enabled",
    };
    const name: string = group.name.toUpperCase();
    const description: string = _.capitalize(group.description);
    const drills: string = translate.t(servicesParameters[group.hasDrills.toString()]);
    const forces: string = translate.t(servicesParameters[group.hasForces.toString()]);

    return { ...group, name, description, drills, forces };
  });

  // Render Elements
  const tableHeaders: IHeaderConfig[] = [
    { align: "center", dataField: "name", header: "Group Name" },
    { align: "center", dataField: "description", header: "Description" },
    { align: "center", dataField: "drills", formatter: statusFormatter, header: "Drills" },
    { align: "center", dataField: "forces", formatter: statusFormatter, header: "Forces" },
    {
      align: "center",
      dataField: "userRole",
      formatter: (value: string) => translate.t(`userModal.roles.${value}`, { defaultValue: "-" }),
      header: "Role",
    },
  ];

  return (
    <React.StrictMode>
      <div className={style.container}>
        <Row>
          <Can do="backend_api_resolvers_project__do_create_project">
            <Col md={2} mdOffset={5}>
              <ButtonToolbar>
                <TooltipWrapper message={translate.t("organization.tabs.groups.newGroup.new.tooltip")}>
                  <Button onClick={openNewProjectModal}>
                    <Glyphicon glyph="plus" />&nbsp;{translate.t("organization.tabs.groups.newGroup.new.text")}
                  </Button>
                </TooltipWrapper>
              </ButtonToolbar>
            </Col>
          </Can>
        </Row>
        {(_.isUndefined(data) || _.isEmpty(data)) ? <React.Fragment /> : (
          <React.Fragment>
            <Row>
              <Col md={12}>
                <Row className={style.content}>
                  <DataTableNext
                    bordered={true}
                    defaultSorted={{ dataField: "name", order: "asc"}}
                    dataset={formatGroupData(data.organization.projects)}
                    exportCsv={false}
                    headers={tableHeaders}
                    id="tblGroups"
                    pageSize={15}
                    rowEvents={{ onClick: handleRowClick }}
                    search={true}
                  />
                </Row>
              </Col>
              <AddProjectModal
                isOpen={isProjectModalOpen}
                organization={organizationName}
                onClose={closeNewProjectModal}
              />
            </Row>
          </React.Fragment>
        )}
      </div>
    </React.StrictMode>
  );
};

export { organizationGroups as OrganizationGroups };
