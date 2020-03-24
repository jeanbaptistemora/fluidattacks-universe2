/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import {
  ButtonToolbar, Col, Glyphicon, Row, ToggleButton, ToggleButtonGroup,
} from "react-bootstrap";
import { Button } from "../../../../components/Button";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import translate from "../../../../utils/translations/translate";
import { AddProjectModal } from "../../components/AddProjectModal";
import { ProjectBox } from "../../components/ProjectBox";
import { default as style } from "./index.css";
import { PROJECTS_QUERY } from "./queries";
import { TagsInfo } from "./TagInfo/index";
import { IHomeViewProps, ITagData, IUserAttr } from "./types";

interface ITagDataTable {
  name: string;
  projects: string;
}

const goToProject: ((projectName: string) => void) = (projectName: string): void => {
  location.hash = `#!/project/${projectName.toUpperCase()}/indicators`;
};

const tableHeaders: IHeader[] = [
  { dataField: "name", header: "Project Name" },
  { dataField: "description", header: "Description" },
];

const handleRowClick: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string }) => void) =
  (event: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string }): void => {
    goToProject(rowInfo.name);
  };

const homeView: React.FC<IHomeViewProps> = (): JSX.Element => {
  const onMount: (() => void) = (): void => {
    mixpanel.track("ProjectHome", {
      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
      User: (window as typeof window & { userName: string }).userName,
    });
  };
  React.useEffect(onMount, []);
  const tableHeadersTags: IHeader[] = [
    { dataField: "name", header: "Tag" },
    { dataField: "projects", header: "Projects" },
  ];

  const [display, setDisplay] = React.useState(_.get(localStorage, "projectsDisplay", "grid"));
  const handleDisplayChange: ((value: string) => void) = (value: string): void => {
    setDisplay(value);
    localStorage.setItem("projectsDisplay", value);
  };

  const [isProjectModalOpen, setProjectModalOpen] = React.useState(false);
  const [isTagModalOpen, setTagModalOpen] = React.useState(false);
  const [tag, setTag] = React.useState("");

  const openNewProjectModal: (() => void) = (): void => {
    setProjectModalOpen(true);
  };
  const closeNewProjectModal: (() => void) = (): void => {
    setProjectModalOpen(false);
  };
  const closeTagModal: (() => void) = (): void => {
    setTagModalOpen(false);
  };
  const displayTag: ((choosedTag: string) => void) = (choosedTag: string): void => {
    setTag(choosedTag);
    setTagModalOpen(true);
  };

  const handleRowTagClick: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string }) => void) =
  (_0: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string }): void => {
    displayTag(rowInfo.name);
  };
  const formatTagDescription: ((projects: Array<{name: string}>) => string) = (
    projects: Array<{name: string}>,
  ): string => (
    projects.map((project: { name: string }) => project.name)
      .join(", ")
  );
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
        {_.includes(["admin"], (window as typeof window & { userRole: string }).userRole) ?
          <Row>
            <Col md={2} mdOffset={5}>
              <ButtonToolbar>
                <Button onClick={openNewProjectModal}>
                  <Glyphicon glyph="plus" />&nbsp;{translate.t("home.newProject.new")}
                </Button>
              </ButtonToolbar>
            </Col>
          </Row>
          : undefined}
        <Query query={PROJECTS_QUERY}>
          {({ data }: QueryResult<IUserAttr>): JSX.Element => {
            if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

            return (
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
                       )}
                  </Row>
                </Col>
                <AddProjectModal isOpen={isProjectModalOpen} onClose={closeNewProjectModal} />
                <TagsInfo isOpen={isTagModalOpen} onClose={closeTagModal} tag={tag} />
              </Row>
            );
          }}
        </Query>
      </div>
    </React.StrictMode>
  );
};

export { homeView as HomeView };
