import mixpanel from "mixpanel-browser";
import React from "react";
import {
  ButtonToolbar, Col, Glyphicon, Row, ToggleButton, ToggleButtonGroup,
} from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable";
import translate from "../../../../utils/translations/translate";
import { ProjectBox } from "../../components/ProjectBox";
import { IDashboardState } from "../../reducer";
import { changeProjectsDisplay, loadProjects, ThunkDispatcher } from "./actions";
import style from "./index.css";

type IHomeViewBaseProps = RouteComponentProps;

interface IHomeViewStateProps {
  displayPreference: IDashboardState["user"]["displayPreference"];
  projects: IDashboardState["user"]["projects"];
}

interface IHomeViewDispatchProps {
  onDisplayChange(value: IDashboardState["user"]["displayPreference"]): void;
  onLoad(): void;
}

type IHomeViewProps = IHomeViewBaseProps & (IHomeViewStateProps & IHomeViewDispatchProps);

const enhance: InferableComponentEnhancer<{}> = lifecycle<IHomeViewProps, {}>({
  componentDidMount(): void {
    mixpanel.track(
      "ProjectHome",
      {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
    this.props.onLoad(); },
});

const homeView: React.FC<IHomeViewProps> = (props: IHomeViewProps): JSX.Element => {

  const goToProject: ((projectName: string) => void) = (projectName: string): void => {
    location.hash = `#!/project/${projectName}/indicators`;
  };

  const renderProjectsGrid: JSX.Element[] = props.projects.map((project: IHomeViewProps["projects"][0]): JSX.Element =>
    (
      <Col md={3}>
        <ProjectBox name={project.name} description={project.description} onClick={goToProject} />
      </Col>
    ),
  );

  const tableHeaders: IHeader[] = [
    { dataField: "name", header: "Project Name", isDate: false, isStatus: false },
    { dataField: "description", header: "Description", isDate: false, isStatus: false },
  ];

  const handleRowClick: ((rowInfo: { name: string }) => void) = (rowInfo: { name: string }): void => {
    goToProject(rowInfo.name);
  };

  const renderProjectsTable: JSX.Element = (
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
      />
      <br />
    </React.Fragment>
  );

  const handleDisplayChange: ((value: {}) => void) = (value: {}): void => {
    props.onDisplayChange(value as IDashboardState["user"]["displayPreference"]);
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
        <Row>
          <Col md={12}>
            <Row className={style.content}>
              {props.displayPreference === "grid" ? renderProjectsGrid : renderProjectsTable}
            </Row>
          </Col>
        </Row>
      </div>
    </React.StrictMode>
  );
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IHomeViewStateProps, IHomeViewBaseProps, IState> =
  (state: IState): IHomeViewStateProps => ({
    displayPreference: state.dashboard.user.displayPreference,
    projects: state.dashboard.user.projects,
  });

const mapDispatchToProps: MapDispatchToProps<IHomeViewDispatchProps, IHomeViewBaseProps> =
  (dispatch: ThunkDispatcher): IHomeViewDispatchProps => ({
    onDisplayChange: (value: IDashboardState["user"]["displayPreference"]): void => {
      dispatch(changeProjectsDisplay(value));
      localStorage.setItem("projectsDisplay", value);
    },
    onLoad: (): void => { dispatch(loadProjects()); },
  });

export = connect(mapStateToProps, mapDispatchToProps)(enhance(homeView));
