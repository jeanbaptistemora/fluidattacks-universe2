import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import {
  ButtonToolbar, Col, Glyphicon, Row, ToggleButton, ToggleButtonGroup,
} from "react-bootstrap";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";
import { Button } from "../../../../components/Button";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeaderConfig } from "../../../../components/DataTableNext/types";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import { Can } from "../../../../utils/authz/Can";
import { useStoredState } from "../../../../utils/hooks";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { AddProjectModal } from "../../components/AddProjectModal";
import { ProjectBox } from "../../components/ProjectBox";
import { default as style } from "../HomeView/index.css";
import { GET_ORGANIZATION_GROUPS } from "./queries";
import { IOrganizationGroups, IOrganizationGroupsProps } from "./types";

const organizationGroups: React.FC<IOrganizationGroupsProps> = (props: IOrganizationGroupsProps): JSX.Element => {
  const { organizationId } = props;
  const { organizationName } = useParams();
  const { url } = useRouteMatch();
  const { push } = useHistory();

  // State management
  const [isProjectModalOpen, setProjectModalOpen] = React.useState(false);
  const [display, setDisplay] = useStoredState("groupsDisplay", { mode: "grid" });

  const openNewProjectModal: (() => void) = (): void => {
    setProjectModalOpen(true);
  };
  const closeNewProjectModal: (() => void) = (): void => {
    setProjectModalOpen(false);
    refetchGroups();
  };
  const handleDisplayChange: ((value: string) => void) = (value: string): void => {
    setDisplay({ mode: value });
  };

  // GraphQL operations
  const { data, refetch: refetchGroups } = useQuery(GET_ORGANIZATION_GROUPS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error("An error occurred loading organization groups", error);
      });
    },
    variables: {
      organizationId,
    },
  });

  // Auxiliary functions
  const goToGroup: ((groupName: string) => void) = (groupName: string): void => {
    push(`${url}/${groupName.toLowerCase()}/analytics`);
  };

  const handleRowClick: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string }) => void) = (
    _0: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string },
  ): void => {
    goToGroup(rowInfo.name);
  };

  // Render Elements
  const tableHeaders: IHeaderConfig[] = [
    { dataField: "name", header: "Group Name" },
    { dataField: "description", header: "Description" },
  ];

  return (
    <React.StrictMode>
      <div className={style.container}>
        <Row>
          <Col sm={12}>
            <ButtonToolbar className={style.displayOptions}>
              <ToggleButtonGroup
                defaultValue="grid"
                name="displayOptions"
                onChange={handleDisplayChange}
                type="radio"
                value={display.mode}
              >
                <ToggleButton value="grid"><Glyphicon glyph="th" /></ToggleButton>
                <ToggleButton value="list"><Glyphicon glyph="th-list" /></ToggleButton>
              </ToggleButtonGroup>
            </ButtonToolbar>
          </Col>
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
                  {display.mode === "grid"
                    ? data.organization.projects.map(
                        (group: IOrganizationGroups["data"]["organization"]["projects"][0], index: number):
                        JSX.Element => (
                          <Col md={3} key={index}>
                            <ProjectBox
                              name={group.name.toUpperCase()}
                              description={group.description}
                              onClick={goToGroup}
                            />
                          </Col>
                      ))
                    : (
                      <DataTableNext
                        bordered={true}
                        dataset={data.organization.projects}
                        exportCsv={false}
                        headers={tableHeaders}
                        id="tblGroups"
                        pageSize={15}
                        rowEvents={{ onClick: handleRowClick }}
                        search={true}
                      />
                    )
                  }
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
