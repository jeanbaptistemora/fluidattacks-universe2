/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import { useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import {
  ButtonToolbar, Col, Glyphicon, Row, ToggleButton, ToggleButtonGroup,
} from "react-bootstrap";
import { useHistory } from "react-router-dom";
import { Button } from "../../../../components/Button";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import { Can } from "../../../../utils/authz/Can";
import { authzPermissionsContext } from "../../../../utils/authz/config";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { AddProjectModal } from "../../components/AddProjectModal";
import { ProjectBox } from "../../components/ProjectBox";
import { default as style } from "./index.css";
import { PROJECTS_QUERY } from "./queries";
import { IHomeViewProps, IOrganizationData, ITagData, IUserAttr } from "./types";

interface ITagDataTable {
  name: string;
  projects: string;
}

const tableHeaders: IHeader[] = [
  { dataField: "name", header: "Project Name" },
  { dataField: "description", header: "Description" },
];

const tableHeadersOrganizations: IHeader[] = [
  { dataField: "name", header: "Organization Name" },
];

const tableHeadersTags: IHeader[] = [
  { dataField: "name", header: "Tag" },
  { dataField: "projects", header: "Projects" },
];

const homeView: React.FC<IHomeViewProps> = (props: IHomeViewProps): JSX.Element => {
  const { setUserRole } = props;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const { push } = useHistory();
  const { userEmail } = (window as typeof window & { userEmail: string });

  const goToProject: ((projectName: string) => void) = (projectName: string): void => {
    push(`/groups/${projectName.toLowerCase()}/indicators`);
  };

  const handleRowClick: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string }) => void) = (
    _0: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string },
  ): void => {
    goToProject(rowInfo.name);
  };

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("ProjectHome", {
      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
      User: (window as typeof window & { userName: string }).userName,
    });
  };
  React.useEffect(onMount, []);

  // State management
  setUserRole(undefined);
  const [display, setDisplay] = React.useState(_.get(localStorage, "projectsDisplay", "grid"));
  const handleDisplayChange: ((value: string) => void) = (value: string): void => {
    setDisplay(value);
    localStorage.setItem("projectsDisplay", value);
  };

  const [isProjectModalOpen, setProjectModalOpen] = React.useState(false);

  const openNewProjectModal: (() => void) = (): void => {
    setProjectModalOpen(true);
  };
  const closeNewProjectModal: (() => void) = (): void => {
    setProjectModalOpen(false);
  };

  // GraphQL operations
  const { data } = useQuery(PROJECTS_QUERY, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error("An error occurred loading projects", error);
      });
    },
    variables: {
      tagsField: permissions.can("backend_api_resolvers_me__get_tags"),
    },
  });

  const displayOrganization: ((choosedOrganization: string) => void) = (choosedOrganization: string): void => {
    const organizations: IOrganizationData[] = data.me.organizations;
    const choosedOrganizationId: string = organizations.filter((organization: IOrganizationData): boolean => (
      organization.name === choosedOrganization.toLowerCase()
    ))[0].id;

    push(`/organizations/${choosedOrganization.toLowerCase()}`);
  };

  const displayTag: ((choosedTag: string) => void) = (choosedTag: string): void => {
    push(`/portfolios/${choosedTag.toLowerCase()}/indicators`);
  };

  const handleRowOrganizationClick: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string }) => void) = (
    _0: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string },
  ): void => {
    displayOrganization(rowInfo.name);
  };

  const handleRowTagClick: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string }) => void) = (
    _0: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string },
  ): void => {
    displayTag(rowInfo.name);
  };

  const formatTagDescription: ((projects: Array<{ name: string }>) => string) = (
    projects: Array<{ name: string }>,
  ): string => {
    const projectsDescription: string = projects.map((project: { name: string }) => project.name)
      .slice(0, 2)
      .join(", ");
    const remaining: number = projects.length - 2;

    return projectsDescription + (remaining > 0 ? translate.t("home.tagResume", {remaining}) : "");
  };
  const formatTagTableData: ((tags: ITagData[]) => ITagDataTable[]) = (tags: ITagData[]): ITagDataTable[] => (
    tags.map((tagMap: ITagData) =>
      ({ name: tagMap.name, projects: formatTagDescription(tagMap.projects) }))
  );

  return (
    <React.StrictMode>
      <div className={style.container}>
        <Row>
          <Col md={10} sm={8}>
            <h2>{translate.t("home.title")}</h2>
          </Col>
          <Col md={2} sm={4}>
            <ButtonToolbar className={style.displayOptions}>
              <ToggleButtonGroup
                defaultValue="grid"
                name="displayOptions"
                onChange={handleDisplayChange}
                type="radio"
                value={display}
              >
                <ToggleButton value="grid"><Glyphicon glyph="th" /></ToggleButton>
                <ToggleButton value="list"><Glyphicon glyph="th-list" /></ToggleButton>
              </ToggleButtonGroup>
            </ButtonToolbar>
          </Col>
        </Row>
        <Can do="backend_api_resolvers_project__do_create_project">
          <Row>
            <Col md={2} mdOffset={5}>
              <ButtonToolbar>
                <TooltipWrapper message={translate.t("home.newGroup.new.tooltip")}>
                  <Button onClick={openNewProjectModal}>
                    <Glyphicon glyph="plus" />&nbsp;{translate.t("home.newGroup.new.text")}
                  </Button>
                </TooltipWrapper>
              </ButtonToolbar>
            </Col>
          </Row>
        </Can>
        {(_.isUndefined(data) || _.isEmpty(data)) ? <React.Fragment /> : (
          <React.Fragment>
            <React.Fragment>
              <Row>
                <Col md={12}>
                  <Row className={style.content}>
                    {display === "grid"
                      ? data.me.projects.map((project: IUserAttr["me"]["projects"][0], index: number): JSX.Element => (
                        <Col md={3} key={index}>
                          <ProjectBox
                            name={project.name.toUpperCase()}
                            description={project.description}
                            onClick={goToProject}
                          />
                        </Col>
                      ))
                      : (
                        <DataTableNext
                          bordered={true}
                          dataset={data.me.projects}
                          exportCsv={false}
                          headers={tableHeaders}
                          id="tblProjects"
                          pageSize={15}
                          remote={false}
                          rowEvents={{ onClick: handleRowClick }}
                          search={true}
                        />
                      )}
                  </Row>
                  {_.isUndefined(data.me.tags) ? undefined : (
                    <React.Fragment>
                      <h2>{translate.t("home.tags")}</h2>
                      <Row className={style.content}>
                        {display === "grid"
                          ? data.me.tags.map((tagMap: IUserAttr["me"]["tags"][0], index: number): JSX.Element => (
                            <Col md={3} key={index}>
                              <ProjectBox
                                name={tagMap.name.toUpperCase()}
                                description={formatTagDescription(tagMap.projects)}
                                onClick={displayTag}
                              />
                            </Col>
                          ))
                          : (
                            <React.Fragment>
                              <DataTableNext
                                bordered={true}
                                dataset={formatTagTableData(data.me.tags)}
                                exportCsv={false}
                                headers={tableHeadersTags}
                                id="tblProjects"
                                pageSize={15}
                                remote={false}
                                rowEvents={{ onClick: handleRowTagClick }}
                                search={true}
                              />
                            </React.Fragment>
                          )}
                      </Row>
                    </React.Fragment>
                  )}
                  {!_.isUndefined(data.me.organizations) ? (
                    <React.Fragment>
                      <h2>{translate.t("home.organizations")}</h2>
                      <Row className={style.content}>
                        {display === "grid"
                          ? data.me.organizations.map(
                              (organizationMap: IUserAttr["me"]["organizations"][0], index: number): JSX.Element => (
                            <Col md={3} key={index}>
                              <ProjectBox
                                name={organizationMap.name.toUpperCase()}
                                description=""
                                onClick={displayOrganization}
                              />
                            </Col>
                          ))
                          : (
                            <React.Fragment>
                              <DataTableNext
                                bordered={true}
                                dataset={data.me.organizations}
                                exportCsv={false}
                                headers={tableHeadersOrganizations}
                                id="tblProjects"
                                pageSize={15}
                                remote={false}
                                rowEvents={{ onClick: handleRowOrganizationClick }}
                                search={true}
                              />
                            </React.Fragment>
                          )}
                      </Row>
                    </React.Fragment>
                  ) : undefined}
                </Col>
                <AddProjectModal isOpen={isProjectModalOpen} onClose={closeNewProjectModal} />
              </Row>
            </React.Fragment>
          </React.Fragment>
        )}
      </div>
    </React.StrictMode>
  );
};

export { homeView as HomeView };
