import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import translate from "../../../../utils/translations/translate";
import { IndicatorBox } from "../../components/IndicatorBox/index";
import { IndicatorGraph } from "../../components/IndicatorGraph/index";
import { IDashboardState } from "../../reducer";
import * as actions from "./actions";
import style from "./index.css";

type IIndicatorsViewBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

type IIndicatorsViewStateProps = IDashboardState["indicators"];

interface IIndicatorsViewDispatchProps {
  onLoad(): void;
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
          <Row>
            <Col md={8} sm={12} xs={12}>
              <Col md={6} sm={12} xs={12}>
                <IndicatorBox
                  icon="findings"
                  name={translate.t("search_findings.tab_indicators.total_findings")}
                  quantity={props.totalFindings}
                  title=""
                  total=""
                />
              </Col>
              <Col md={6} sm={12} xs={12}>
                <IndicatorBox
                  icon="vulnerabilities"
                  name={translate.t("search_findings.tab_indicators.total_vulnerabilitites")}
                  quantity={totalVulnerabilities}
                  title=""
                  total=""
                />
              </Col>
              <Col md={6} sm={12} xs={12}>
                <IndicatorBox
                  icon="totalVulnerabilities"
                  name={translate.t("search_findings.tab_indicators.pending_closing_check")}
                  quantity={props.pendingClosingCheck}
                  title=""
                  total=""
                />
              </Col>
              <Col md={6} sm={12} xs={12}>
                <IndicatorBox
                  icon="calendar"
                  name={translate.t("search_findings.tab_indicators.last_closing_vuln")}
                  quantity={props.lastClosingVuln}
                  title=""
                  total=""
                />
              </Col>
              <Col md={6} sm={12} xs={12}>
                <IndicatorBox
                  icon="integrityHigh"
                  name={translate.t("search_findings.tab_indicators.undefined_treatment")}
                  quantity={props.totalTreatment.undefined}
                  title=""
                  total=""
                />
              </Col>
              <Col md={6} sm={12} xs={12}>
                <IndicatorBox
                  icon="graph"
                  name={translate.t("search_findings.tab_indicators.mean_remediate")}
                  quantity={props.meanRemediate}
                  title=""
                  total={translate.t("search_findings.tab_indicators.days")}
                />
              </Col>
              <Col md={6} sm={12} xs={12}>
                <IndicatorBox
                  icon="vectorLocal"
                  name={translate.t("search_findings.tab_indicators.max_severity")}
                  quantity={props.maxSeverity}
                  title=""
                  total="/10"
                />
              </Col>
              <Col md={6} sm={12} xs={12}>
                <IndicatorBox
                  icon="openVulnerabilities"
                  name={translate.t("search_findings.tab_indicators.max_open_severity")}
                  quantity={props.maxOpenSeverity}
                  title=""
                  total="/10"
                />
              </Col>
            </Col>
            <Col md={4} sm={12} xs={12}>
              <Col md={12} sm={12} xs={12} className={style.box_size}>
                <IndicatorGraph
                  data={statusGraph(props)}
                  name={translate.t("search_findings.tab_indicators.status_graph")}
                />
              </Col>
              <Col md={12} sm={12} xs={12} className={style.box_size}>
                <IndicatorGraph
                  data={treatmentGraph(props)}
                  name={translate.t("search_findings.tab_indicators.treatment_graph")}
                />
              </Col>
            </Col>
          </Row>
        </Col>
      </Row>
      <br />
      <br />
      <hr />
      <Row>
        <Col md={12} sm={12} xs={12}>
          <h1 className={style.title}>{translate.t("search_findings.tab_indicators.git_title")}</h1>
          <Col md={4} sm={12} xs={12}>
            <IndicatorBox
              icon="integrityNone"
              name={translate.t("search_findings.tab_indicators.repositories")}
              quantity={props.repositories.length}
              title=""
              total=""
            />
          </Col>
          <Col md={4} sm={12} xs={12}>
            <IndicatorBox
              icon="authors"
              name={translate.t("search_findings.tab_indicators.authors")}
              quantity={props.currentMonthAuthors}
              title=""
              total=""
            />
          </Col>
          <Col md={4} sm={12} xs={12}>
            <IndicatorBox
              icon="terminal"
              name={translate.t("search_findings.tab_indicators.commits")}
              quantity={props.currentMonthCommits}
              title=""
              total=""
            />
          </Col>
        </Col>
      </Row>
    </React.StrictMode>
  );
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IIndicatorsViewStateProps, IIndicatorsViewProps, IState> =
  (state: IState): IIndicatorsViewStateProps => ({
    closedVulnerabilities: state.dashboard.indicators.closedVulnerabilities,
    currentMonthAuthors: state.dashboard.indicators.currentMonthAuthors,
    currentMonthCommits: state.dashboard.indicators.currentMonthCommits,
    lastClosingVuln: state.dashboard.indicators.lastClosingVuln,
    maxOpenSeverity: state.dashboard.indicators.maxOpenSeverity,
    maxSeverity: state.dashboard.indicators.maxSeverity,
    meanRemediate: state.dashboard.indicators.meanRemediate,
    openVulnerabilities: state.dashboard.indicators.openVulnerabilities,
    pendingClosingCheck: state.dashboard.indicators.pendingClosingCheck,
    repositories: state.dashboard.indicators.repositories,
    totalFindings: state.dashboard.indicators.totalFindings,
    totalTreatment: state.dashboard.indicators.totalTreatment,
  });

const mapDispatchToProps: MapDispatchToProps<IIndicatorsViewDispatchProps, IIndicatorsViewBaseProps> =
  (dispatch: actions.ThunkDispatcher, ownProps: IIndicatorsViewBaseProps): IIndicatorsViewDispatchProps => {
    const { projectName } = ownProps.match.params;

    return ({
      onLoad: (): void => { dispatch(actions.loadIndicators(projectName)); },
    });
  };

export = connect(mapStateToProps, mapDispatchToProps)(enhance(indicatorsView));
