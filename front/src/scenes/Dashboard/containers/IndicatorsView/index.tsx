import _ from "lodash";
import React from "react";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { Button } from "../../../../components/Button/index";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { addTagsModal as AddTagsModal } from "../../components/AddTagsModal/index";
import { IndicatorBox } from "../../components/IndicatorBox/index";
import { IndicatorGraph } from "../../components/IndicatorGraph/index";
import { IDashboardState } from "../../reducer";
import * as actions from "./actions";
import style from "./index.css";

type IIndicatorsViewBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

type IIndicatorsViewStateProps = IDashboardState["indicators"];

interface IIndicatorsViewDispatchProps {
  onCloseAddModal(): void;
  onLoad(): void;
  onOpenAddModal(): void;
  onRemoveTag(tag: string): void;
  onSaveTags(tags: IIndicatorsViewStateProps["tagsDataset"]): void;
}

type IIndicatorsViewProps = IIndicatorsViewBaseProps & (IIndicatorsViewStateProps & IIndicatorsViewDispatchProps);

interface IGraphData {
  backgroundColor: string[];
  data: number[];
  hoverBackgroundColor: string[];
}

const enhance: InferableComponentEnhancer<{}> = lifecycle<IIndicatorsViewProps, {}>({
  componentDidMount(): void { this.props.onLoad(); },
});

const removeTag: ((props: IIndicatorsViewProps) => void) = (props: IIndicatorsViewProps): void => {
  const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblTags tr input:checked");
  if (selectedQry.length > 0) {
    if (selectedQry[0].closest("tr") !== null) {
      const selectedRow: Element = selectedQry[0].closest("tr") as Element;
      const tag: string | null = selectedRow.children[1].textContent;
      props.onRemoveTag(String(tag));
    } else {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred removing tags");
    }
  } else {
    msgError(translate.t("search_findings.tab_resources.no_selection"));
  }
};

const saveTags: ((tags: IIndicatorsViewProps["tagsDataset"], props: IIndicatorsViewProps) => void) =
  (tags: IIndicatorsViewProps["tagsDataset"], props: IIndicatorsViewProps): void => {
    let containsRepeated: boolean;
    containsRepeated = tags.filter(
      (newItem: IIndicatorsViewProps["tagsDataset"][0]) => _.findIndex(
        props.tagsDataset,
        (currentItem: IIndicatorsViewProps["tagsDataset"][0]) =>
          currentItem === newItem,
      ) > -1).length > 0;
    if (containsRepeated) {
      msgError(translate.t("search_findings.tab_resources.repeated_item"));
    } else {
      props.onSaveTags(tags);
    }
  };
/* tslint:disable-next-line:no-unused-variable
 * Disable this rule because this code will be removed in the next MR
 */
const renderTagsView: ((props: IIndicatorsViewProps) => JSX.Element) = (props: IIndicatorsViewProps): JSX.Element => {
  const tagsDataset: Array<{ tagName: string }> = props.tagsDataset.map((tagName: string) => ({ tagName }));

  const handleOpenAddModal: (() => void) = (): void => { props.onOpenAddModal(); };
  const handleCloseAddModal: (() => void) = (): void => { props.onCloseAddModal(); };
  const handleRemoveTagClick: (() => void) = (): void => { removeTag(props); };
  const handleSubmit: ((values: { tags: IIndicatorsViewProps["tagsDataset"] }) => void) =
    (values: { tags: IIndicatorsViewProps["tagsDataset"] }): void => { saveTags(values.tags, props); };

  return (
    <React.Fragment>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <Row>
            <Col md={12} sm={12} xs={12}>
              <Row>
                <Col md={12}>
                  <Col mdOffset={4} md={2} sm={6}>
                    <Button id="addTag" block={true} bsStyle="primary" onClick={handleOpenAddModal}>
                      <Glyphicon glyph="plus" />&nbsp;
                      {translate.t("search_findings.tab_resources.add_repository")}
                    </Button>
                  </Col>
                  <Col md={2} sm={6}>
                    <Button id="removeTag" block={true} bsStyle="primary" onClick={handleRemoveTagClick}>
                      <Glyphicon glyph="minus" />&nbsp;
                      {translate.t("search_findings.tab_resources.remove_repository")}
                    </Button>
                  </Col>
                </Col>
              </Row>
              <Row>
                <Col md={12} sm={12}>
                  <DataTable
                    dataset={tagsDataset}
                    enableRowSelection={true}
                    exportCsv={false}
                    search={false}
                    headers={[{ dataField: "tagName", header: "Tags", isDate: false, isStatus: false }]}
                    id="tblTags"
                    pageSize={15}
                    title={""}
                  />
                </Col>
              </Row>
            </Col>
          </Row>
        </Col>
      </Row>
      <AddTagsModal isOpen={props.addModal.open} onClose={handleCloseAddModal} onSubmit={handleSubmit} />
    </React.Fragment>
  );
};

const calcPercent: ((value: number, total: number) => number) = (value: number, total: number): number =>
  _.round(value * 100 / total, 1);

const statusGraph: ((props: IIndicatorsViewProps) => { [key: string]: string | string[] | IGraphData[]}) =
(props: IIndicatorsViewProps): { [key: string]: string | string[] | IGraphData[]} => {
  const statusDataset: IGraphData = {
    backgroundColor: ["#ff1a1a", "#27BF4F"],
    data: [props.openVulnerabilities, props.closedVulnerabilities],
    hoverBackgroundColor: ["#e51414", "#069D2E"],
  };
  const totalVulnerabilities: number = props.openVulnerabilities + props.closedVulnerabilities;
  const openPercent: number = calcPercent(props.openVulnerabilities, totalVulnerabilities);
  const closedPercent: number = calcPercent(props.closedVulnerabilities, totalVulnerabilities);
  const statusGraphData: { [key: string]: string | string[] | IGraphData[]} = {
    datasets: [statusDataset],
    labels: [`${openPercent}% ${translate.t("search_findings.tab_indicators.open")}`,
             `${closedPercent}% ${translate.t("search_findings.tab_indicators.closed")}`],
  };

  return statusGraphData;
};

const treatmentGraph: ((props: IIndicatorsViewProps) => { [key: string]: string | string[] | IGraphData[]}) =
(props: IIndicatorsViewProps): { [key: string]: string | string[] | IGraphData[]} => {
  const treatmentDataset: IGraphData = {
    backgroundColor: ["#b7b7b7", "#FFAA63", "#CD2A86"],
    data: [props.totalTreatment.accepted, props.totalTreatment.inProgress, props.totalTreatment.undefined],
    hoverBackgroundColor: ["#999797", "#FF9034", "#A70762"],
  };
  const acceptedPercent: number = calcPercent(props.totalTreatment.accepted, props.openVulnerabilities);
  const inProgressPercent: number = calcPercent(props.totalTreatment.inProgress, props.openVulnerabilities);
  const undefinedPercent: number = calcPercent(props.totalTreatment.undefined, props.openVulnerabilities);
  const treatmentGraphData: { [key: string]: string | string[] | IGraphData[]} = {
    datasets: [treatmentDataset],
    labels: [`${acceptedPercent}% ${translate.t("search_findings.tab_indicators.treatment_accepted")}`,
             `${inProgressPercent}% ${translate.t("search_findings.tab_indicators.treatment_in_progress")}`,
             `${undefinedPercent}% ${translate.t("search_findings.tab_indicators.treatment_no_defined")}`],
  };

  return treatmentGraphData;
};

const indicatorsView: React.SFC<IIndicatorsViewProps> = (props: IIndicatorsViewProps): JSX.Element => {
  const totalVulnerabilities: number = props.openVulnerabilities + props.closedVulnerabilities;

  return (
    <React.StrictMode>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <h1 className={style.title}>{translate.t("search_findings.tab_indicators.project_title")}</h1>
          <IndicatorBox
            icon="findings"
            name={translate.t("search_findings.tab_indicators.total_findings")}
            quantity={props.totalFindings}
            title=""
            total=""
          />
          <IndicatorBox
            icon="vulnerabilities"
            name={translate.t("search_findings.tab_indicators.total_vulnerabilitites")}
            quantity={totalVulnerabilities}
            title=""
            total=""
          />
          <IndicatorBox
            icon="totalVulnerabilities"
            name={translate.t("search_findings.tab_indicators.pending_closing_check")}
            quantity={props.pendingClosingCheck}
            title=""
            total=""
          />
          <IndicatorBox
            icon="calendar"
            name={translate.t("search_findings.tab_indicators.last_closing_vuln")}
            quantity={props.lastClosingVuln}
            title=""
            total=""
          />
          <IndicatorBox
            icon="integrityHigh"
            name={translate.t("search_findings.tab_indicators.undefined_treatment")}
            quantity={props.totalTreatment.undefined}
            title=""
            total=""
          />
          <IndicatorBox
            icon="graph"
            name={translate.t("search_findings.tab_indicators.mean_remediate")}
            quantity={props.meanRemediate}
            title=""
            total={translate.t("search_findings.tab_indicators.days")}
          />
          <IndicatorBox
            icon="vectorLocal"
            name={translate.t("search_findings.tab_indicators.max_severity")}
            quantity={props.maxSeverity}
            title=""
            total="/10"
          />
          <IndicatorBox
            icon="openVulnerabilities"
            name={translate.t("search_findings.tab_indicators.max_open_severity")}
            quantity={props.maxOpenSeverity}
            title=""
            total="/10"
          />
        </Col>
      </Row>
      <br />
      <Row>
        <IndicatorGraph
          data={statusGraph(props)}
          name={translate.t("search_findings.tab_indicators.status_graph")}
        />
        <IndicatorGraph
          data={treatmentGraph(props)}
          name={translate.t("search_findings.tab_indicators.treatment_graph")}
        />
      </Row>
      <br />
      <hr />
      <Row>
        <Col md={12} sm={12} xs={12}>
          <h1 className={style.title}>{translate.t("search_findings.tab_indicators.git_title")}</h1>
          <IndicatorBox
            icon="integrityNone"
            name={translate.t("search_findings.tab_indicators.repositories")}
            quantity={props.repositories.length}
            title=""
            total=""
          />
          <IndicatorBox
            icon="authors"
            name={translate.t("search_findings.tab_indicators.authors")}
            quantity={props.currentMonthAuthors}
            title=""
            total=""
          />
          <IndicatorBox
            icon="terminal"
            name={translate.t("search_findings.tab_indicators.commits")}
            quantity={props.currentMonthCommits}
            title=""
            total=""
          />
        </Col>
      </Row>
    </React.StrictMode>
  );
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IIndicatorsViewStateProps, IIndicatorsViewProps, IState> =
  (state: IState): IIndicatorsViewStateProps => ({
    addModal: state.dashboard.indicators.addModal,
    closedVulnerabilities: state.dashboard.indicators.closedVulnerabilities,
    currentMonthAuthors: state.dashboard.indicators.currentMonthAuthors,
    currentMonthCommits: state.dashboard.indicators.currentMonthCommits,
    deletionDate: state.dashboard.indicators.deletionDate,
    lastClosingVuln: state.dashboard.indicators.lastClosingVuln,
    maxOpenSeverity: state.dashboard.indicators.maxOpenSeverity,
    maxSeverity: state.dashboard.indicators.maxSeverity,
    meanRemediate: state.dashboard.indicators.meanRemediate,
    openVulnerabilities: state.dashboard.indicators.openVulnerabilities,
    pendingClosingCheck: state.dashboard.indicators.pendingClosingCheck,
    repositories: state.dashboard.indicators.repositories,
    subscription: state.dashboard.indicators.subscription,
    tagsDataset: state.dashboard.indicators.tagsDataset,
    totalFindings: state.dashboard.indicators.totalFindings,
    totalTreatment: state.dashboard.indicators.totalTreatment,
  });

const mapDispatchToProps: MapDispatchToProps<IIndicatorsViewDispatchProps, IIndicatorsViewBaseProps> =
  (dispatch: actions.ThunkDispatcher, ownProps: IIndicatorsViewBaseProps): IIndicatorsViewDispatchProps => {
    const { projectName } = ownProps.match.params;

    return ({
      onCloseAddModal: (): void => { dispatch(actions.closeAddModal()); },
      onLoad: (): void => { dispatch(actions.loadIndicators(projectName)); },
      onOpenAddModal: (): void => { dispatch(actions.openAddModal()); },
      onRemoveTag: (tag: string): void => { dispatch(actions.removeTag(projectName, tag)); },
      onSaveTags: (tags: IIndicatorsViewProps["tagsDataset"]): void => {
        dispatch(actions.saveTags(projectName, tags));
      },
    });
  };

export = connect(mapStateToProps, mapDispatchToProps)(enhance(indicatorsView));
