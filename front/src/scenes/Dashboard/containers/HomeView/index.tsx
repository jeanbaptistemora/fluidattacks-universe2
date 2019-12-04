/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Query, QueryResult } from "react-apollo";
import {
  ButtonToolbar, Col, Glyphicon, Row, ToggleButton, ToggleButtonGroup,
} from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { ProjectBox } from "../../components/ProjectBox";
import { IDashboardState } from "../../reducer";
import { changeProjectsDisplay, ThunkDispatcher } from "./actions";
import { default as style } from "./index.css";
import { PROJECTS_QUERY } from "./queries";
import { IHomeViewBaseProps, IHomeViewDispatchProps, IHomeViewProps,
  IHomeViewStateProps, IState, IUserAttr } from "./types";

const goToProject: ((projectName: string) => void) = (projectName: string): void => {
  location.hash = `#!/project/${projectName}/indicators`;
};

const renderProjectsGrid: ((props: IUserAttr["me"]) => JSX.Element[]) =
  (props: IUserAttr["me"]): JSX.Element[] =>
    props.projects.map((project: IUserAttr["me"]["projects"][0]) =>
      (
        <Col md={3}>
          <ProjectBox name={project.name} description={project.description} onClick={goToProject} />
        </Col>
      ));

const tableHeaders: IHeader[] = [
  { dataField: "name", header: "Project Name", isDate: false, isStatus: false },
  { dataField: "description", header: "Description", isDate: false, isStatus: false },
];

const handleRowClick: ((rowInfo: { name: string }) => void) = (rowInfo: { name: string }): void => {
  goToProject(rowInfo.name);
};

const renderProjectsTable: ((props: IUserAttr["me"]) => JSX.Element) =
  (props: IUserAttr["me"]): JSX.Element => (
    <React.Fragment>
      <DataTable
        dataset={props.projects}
        enableRowSelection={false}
        exportCsv={false}
        headers={tableHeaders}
        id="tblProjects"
        onClickRow={handleRowClick}
        pageSize={15}
        search={true}
        selectionMode="none"
      />
      <br />
    </React.Fragment>
  );

const homeView: React.FC<IHomeViewProps> = (props: IHomeViewProps): JSX.Element => {
  const handleDisplayChange: ((value: {}) => void) = (value: {}): void => {
    props.onDisplayChange(value as IDashboardState["user"]["displayPreference"]);
  };

  const handleQryResult: ((qrResult: IUserAttr) => void) = (qrResult: IUserAttr): void => {
    mixpanel.track(
      "ProjectHome",
      {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
    hidePreloader();
  };

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
                value={props.displayPreference}
              >
                <ToggleButton value="grid"><Glyphicon glyph="th" /></ToggleButton>
                <ToggleButton value="list"><Glyphicon glyph="th-list" /></ToggleButton>
              </ToggleButtonGroup>
            </ButtonToolbar>
          </Col>
        </Row>
        <Query query={PROJECTS_QUERY} onCompleted={handleQryResult}>
          {
            ({loading, error, data}: QueryResult<IUserAttr>): React.ReactNode => {
              if (loading) {
                showPreloader();

                return <React.Fragment/>;
              }
              if (!_.isUndefined(error)) {
                hidePreloader();
                handleGraphQLErrors("An error occurred getting project list", error);

                return <React.Fragment/>;
              }
              if (!_.isUndefined(data)) {
                data.me.projects = data.me.projects.map((project: { description: string; name: string }) => ({
                  ...project, name: project.name.toUpperCase(),
                }));

                return (
                  <Row>
                    <Col md={12}>
                      <Row className={style.content}>
                        {props.displayPreference === "grid"
                          ? renderProjectsGrid(data.me) : renderProjectsTable(data.me)
                        }
                      </Row>
                    </Col>
                  </Row>
                );
              }
            }}
        </Query>
      </div>
    </React.StrictMode>
  );
};

const mapStateToProps: MapStateToProps<IHomeViewStateProps, IHomeViewBaseProps, IState> =
  (state: IState): IHomeViewStateProps => ({
    displayPreference: state.dashboard.user.displayPreference,
  });

const mapDispatchToProps: MapDispatchToProps<IHomeViewDispatchProps, IHomeViewBaseProps> =
  (dispatch: ThunkDispatcher): IHomeViewDispatchProps => ({
    onDisplayChange: (value: IDashboardState["user"]["displayPreference"]): void => {
      dispatch(changeProjectsDisplay(value));
      localStorage.setItem("projectsDisplay", value);
    },
  });

export = connect(mapStateToProps, mapDispatchToProps)(homeView);
