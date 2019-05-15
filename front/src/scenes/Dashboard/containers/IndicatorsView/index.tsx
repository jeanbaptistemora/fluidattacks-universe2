/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import gql from "graphql-tag";
import _ from "lodash";
import React from "react";
import { Query, QueryResult } from "react-apollo";
import { Col, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { IndicatorBox } from "../../components/IndicatorBox/index";
import { IndicatorGraph } from "../../components/IndicatorGraph/index";
import style from "./index.css";

type IIndicatorsViewBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

interface IIndicatorsProps {
  project: {
    closedVulnerabilities: number;
    currentMonthAuthors: number;
    currentMonthCommits: number;
    lastClosingVuln: number;
    maxOpenSeverity: number;
    maxSeverity: number;
    meanRemediate: number;
    openVulnerabilities: number;
    pendingClosingCheck: number;
    totalFindings: number;
    totalTreatment: string;
  };
  resources: {
    repositories: string;
  };
}

type IIndicatorsViewProps = IIndicatorsViewBaseProps & IIndicatorsProps;

interface IGraphData {
  backgroundColor: string[];
  data: number[];
  hoverBackgroundColor: string[];
}

const calcPercent: ((value: number, total: number) => number) = (value: number, total: number): number =>
  _.round(value * 100 / total, 1);

const statusGraph: ((props: IIndicatorsViewProps["project"]) => { [key: string]: string | string[] | IGraphData[]}) =
(props: IIndicatorsViewProps["project"]): { [key: string]: string | string[] | IGraphData[]} => {
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

const treatmentGraph: ((props: IIndicatorsViewProps["project"]) => { [key: string]: string | string[] | IGraphData[]}) =
(props: IIndicatorsViewProps["project"]): { [key: string]: string | string[] | IGraphData[]} => {
  const totalTreatment: { [key: string]: number } = JSON.parse(props.totalTreatment);
  const treatmentDataset: IGraphData = {
    backgroundColor: ["#b7b7b7", "#FFAA63", "#CD2A86"],
    data: [totalTreatment.accepted, totalTreatment.inProgress, totalTreatment.undefined],
    hoverBackgroundColor: ["#999797", "#FF9034", "#A70762"],
  };
  const acceptedPercent: number = calcPercent(totalTreatment.accepted, props.openVulnerabilities);
  const inProgressPercent: number = calcPercent(totalTreatment.inProgress, props.openVulnerabilities);
  const undefinedPercent: number = calcPercent(totalTreatment.undefined, props.openVulnerabilities);
  const treatmentGraphData: { [key: string]: string | string[] | IGraphData[]} = {
    datasets: [treatmentDataset],
    labels: [`${acceptedPercent}% ${translate.t("search_findings.tab_indicators.treatment_accepted")}`,
             `${inProgressPercent}% ${translate.t("search_findings.tab_indicators.treatment_in_progress")}`,
             `${undefinedPercent}% ${translate.t("search_findings.tab_indicators.treatment_no_defined")}`],
  };

  return treatmentGraphData;
};

const indicatorsView: React.FC<IIndicatorsViewProps> = (props: IIndicatorsViewProps): JSX.Element => {
  const projectName: string = props.match.params.projectName;

  return (
    <Query
      query={gql`
        {
          project(projectName: "${projectName}"){
            closedVulnerabilities
            currentMonthAuthors
            currentMonthCommits
            lastClosingVuln
            maxOpenSeverity
            maxSeverity
            meanRemediate
            openVulnerabilities
            pendingClosingCheck
            totalFindings
            totalTreatment
          }
          resources(projectName: "${projectName}"){
            repositories
          }
        }
      `}
    >
      {
        ({loading, error, data}: QueryResult<IIndicatorsViewProps>): React.ReactNode => {
          if (loading) {
            showPreloader();

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            hidePreloader();
            if (_.includes(["Login required", "Exception - Invalid Authorization"], error.message)) {
              location.assign("/integrates/logout");
            } else if (error.message === "Access denied") {
              msgError(translate.t("proj_alerts.access_denied"));
            } else {
              msgError(translate.t("proj_alerts.error_textsad"));
              rollbar.error(error.message, error);
            }

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data)) {
            const totalVulnerabilities: number =
              data.project.openVulnerabilities + data.project.closedVulnerabilities;
            const undefinedTreatment: number = JSON.parse(data.project.totalTreatment).undefined;
            hidePreloader();

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
                            quantity={data.project.totalFindings}
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
                            quantity={data.project.pendingClosingCheck}
                            title=""
                            total=""
                          />
                        </Col>
                        <Col md={6} sm={12} xs={12}>
                          <IndicatorBox
                            icon="calendar"
                            name={translate.t("search_findings.tab_indicators.last_closing_vuln")}
                            quantity={data.project.lastClosingVuln}
                            title=""
                            total=""
                          />
                        </Col>
                        <Col md={6} sm={12} xs={12}>
                          <IndicatorBox
                            icon="integrityHigh"
                            name={translate.t("search_findings.tab_indicators.undefined_treatment")}
                            quantity={undefinedTreatment}
                            title=""
                            total=""
                          />
                        </Col>
                        <Col md={6} sm={12} xs={12}>
                          <IndicatorBox
                            icon="graph"
                            name={translate.t("search_findings.tab_indicators.mean_remediate")}
                            quantity={data.project.meanRemediate}
                            title=""
                            total={translate.t("search_findings.tab_indicators.days")}
                          />
                        </Col>
                        <Col md={6} sm={12} xs={12}>
                          <IndicatorBox
                            icon="vectorLocal"
                            name={translate.t("search_findings.tab_indicators.max_severity")}
                            quantity={data.project.maxSeverity}
                            title=""
                            total="/10"
                          />
                        </Col>
                        <Col md={6} sm={12} xs={12}>
                          <IndicatorBox
                            icon="openVulnerabilities"
                            name={translate.t("search_findings.tab_indicators.max_open_severity")}
                            quantity={data.project.maxOpenSeverity}
                            title=""
                            total="/10"
                          />
                        </Col>
                      </Col>
                      <Col md={4} sm={12} xs={12}>
                        <Col md={12} sm={12} xs={12} className={style.box_size}>
                          <IndicatorGraph
                            data={statusGraph(data.project)}
                            name={translate.t("search_findings.tab_indicators.status_graph")}
                          />
                        </Col>
                        <Col md={12} sm={12} xs={12} className={style.box_size}>
                          <IndicatorGraph
                            data={treatmentGraph(data.project)}
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
                        quantity={JSON.parse(data.resources.repositories).length}
                        title=""
                        total=""
                      />
                    </Col>
                    <Col md={4} sm={12} xs={12}>
                      <IndicatorBox
                        icon="authors"
                        name={translate.t("search_findings.tab_indicators.authors")}
                        quantity={data.project.currentMonthAuthors}
                        title=""
                        total=""
                      />
                    </Col>
                    <Col md={4} sm={12} xs={12}>
                      <IndicatorBox
                        icon="terminal"
                        name={translate.t("search_findings.tab_indicators.commits")}
                        quantity={data.project.currentMonthCommits}
                        title=""
                        total=""
                      />
                    </Col>
                  </Col>
                </Row>
              </React.StrictMode>
            );
          }
        }}
    </Query>
  );
};

export { indicatorsView as ProjectIndicatorsView };
