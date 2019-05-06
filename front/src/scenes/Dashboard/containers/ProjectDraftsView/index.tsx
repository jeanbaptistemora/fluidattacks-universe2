import mixpanel from "mixpanel-browser";
import React from "react";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable/index";
import { formatDrafts } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { IDashboardState } from "../../reducer";
import { loadFindingsData, ThunkDispatcher } from "./actions";

type IProjectDraftsBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

type IProjectDraftsStateProps = IDashboardState["drafts"];

interface IProjectDraftsDispatchProps {
  onLoad(): void;
}

type IProjectDraftsProps = IProjectDraftsBaseProps & (IProjectDraftsStateProps & IProjectDraftsDispatchProps);

const enhance: InferableComponentEnhancer<{}> = lifecycle<IProjectDraftsProps, {}>({
  componentDidMount(): void { this.props.onLoad(); mixpanel.track("ProjectDrafts"); },
});

const tableHeaders: IHeader[] = [
  { align: "center", dataField: "reportDate", header: "Date", isDate: false, isStatus: false, width: "10%" },
  { align: "center", dataField: "type", header: "Type", isDate: false, isStatus: false, width: "8%" },
  { align: "center", dataField: "title", header: "Title", isDate: false, isStatus: false, wrapped: true, width: "18%" },
  {
    align: "center", dataField: "description", header: "Description", isDate: false, isStatus: false, width: "30%",
    wrapped: true,
  },
  { align: "center", dataField: "severityScore", header: "Severity", isDate: false, isStatus: false, width: "8%" },
  {
    align: "center", dataField: "openVulnerabilities", header: "Open Vulns.", isDate: false, isStatus: false,
    width: "6%",
  },
  { align: "center", dataField: "isExploitable", header: "Exploitable", isDate: false, isStatus: false, width: "10%" },
  { align: "center", dataField: "isReleased", header: "Released", isDate: false, isStatus: false, width: "10%" },
];

const projectDraftsView: React.FC<IProjectDraftsProps> = (props: IProjectDraftsProps): JSX.Element => {
  const { projectName } = props.match.params;

  const goToFinding: ((rowInfo: { id: string }) => void) = (rowInfo: { id: string }): void => {
    mixpanel.track("ReadDraft");
    location.hash = `#!/project/${projectName}/${rowInfo.id}/description`;
  };

  return (
    <React.StrictMode>
      <p>{translate.t("project.findings.help_label")}</p>
      <DataTable
        dataset={formatDrafts(props.dataset)}
        enableRowSelection={false}
        exportCsv={true}
        headers={tableHeaders}
        id="tblDrafts"
        onClickRow={goToFinding}
        pageSize={15}
        search={true}
      />
    </React.StrictMode>
  );
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IProjectDraftsStateProps, IProjectDraftsBaseProps, IState> =
  (state: IState): IProjectDraftsStateProps => ({
    ...state.dashboard.drafts,
  });

const mapDispatchToProps: MapDispatchToProps<IProjectDraftsDispatchProps, IProjectDraftsBaseProps> =
  (dispatch: ThunkDispatcher, ownProps: IProjectDraftsBaseProps): IProjectDraftsDispatchProps => {
    const { projectName } = ownProps.match.params;

    return ({
      onLoad: (): void => { dispatch(loadFindingsData(projectName)); },
    });
  };

export = connect(mapStateToProps, mapDispatchToProps)(enhance(projectDraftsView));
