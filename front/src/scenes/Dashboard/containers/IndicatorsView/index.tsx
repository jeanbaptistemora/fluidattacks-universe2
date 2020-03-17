/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import { LineDatum } from "@nivo/line";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { IndicatorBox } from "../../components/IndicatorBox/index";
import { IndicatorChart } from "../../components/IndicatorChart";
import { IndicatorGraph } from "../../components/IndicatorGraph/index";
import { default as style } from "./index.css";
import { GET_INDICATORS } from "./queries";
import { IForcesExecution, IGraphData, IIndicatorsProps, IIndicatorsViewBaseProps } from "./types";

const calcPercent: ((value: number, total: number) => number) = (value: number, total: number): number =>
  _.round(value * 100 / total, 1);

const statusGraph: ((props: IIndicatorsProps["project"]) => { [key: string]: string | string[] | IGraphData[]}) =
(props: IIndicatorsProps["project"]): { [key: string]: string | string[] | IGraphData[]} => {
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

const treatmentGraph: ((props: IIndicatorsProps["project"]) => { [key: string]: string | string[] | IGraphData[]}) =
(props: IIndicatorsProps["project"]): { [key: string]: string | string[] | IGraphData[]} => {
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

const indicatorsView: React.FC<IIndicatorsViewBaseProps> = (props: IIndicatorsViewBaseProps): JSX.Element => {
  const projectName: string = props.match.params.projectName;

  const goToProjectFindings: (() => void) = (): void => {
    location.hash = `#!/project/${projectName}/findings`;
  };

  const goToProjectForces: (() => void) = (): void => {
    location.hash = `#!/project/${projectName}/forces`;
  };

  const goToProjectSettings: (() => void) = (): void => {
    location.hash = `#!/project/${projectName}/resources`;
  };

  const handleQryResult: ((qrResult: IIndicatorsProps) => void) = (qrResult: IIndicatorsProps): void => {
    mixpanel.track(
      "ProjectIndicator",
      {
        Organization: (window as typeof window & { userOrganization: string }).userOrganization,
        User: (window as typeof window & { userName: string }).userName,
      });
  };

  return (
    <Query query={GET_INDICATORS} variables={{ projectName }} onCompleted={handleQryResult}>
      {
        ({ error, data, refetch }: QueryResult<IIndicatorsProps>): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) {

            return <React.Fragment />;
          }
          if (!_.isUndefined(error)) {
            handleGraphQLErrors("An error occurred getting indicators", error);

            return <React.Fragment />;
          }
          if (!_.isUndefined(data)) {
            const totalVulnerabilities: number =
              _.sum([data.project.openVulnerabilities, data.project.closedVulnerabilities]);
            const undefinedTreatment: number = JSON.parse(data.project.totalTreatment).undefined;
            const dataChart: LineDatum[][] = JSON.parse(data.project.remediatedOverTime);

            const executions: [IForcesExecution] = data.forcesExecutions.executions;
            const executionsInAnyMode: number = executions.length;
            const executionsInStrictMode: number =
              executions.filter((execution: IForcesExecution): boolean => execution.strictness === "strict").length;

            const securityCommitmentNumber: number =
              _.round(executionsInAnyMode > 0 ? executionsInStrictMode / executionsInAnyMode * 100 : 100, 0);
            const securityCommitment: string = `${securityCommitmentNumber}%`;

            return (
              <React.StrictMode>
                <Row>
                  <Col md={12} sm={12} xs={12}>
                    <h1 className={style.title}>{translate.t("search_findings.tab_indicators.project_title")}</h1>
                    {dataChart.length > 0 ? (
                      <IndicatorChart
                        dataChart={dataChart}
                      />
                    ) : undefined}
                  </Col>
                </Row>
                <Row>
                  <Col md={12} sm={12} xs={12}>
                    <Row>
                      <Col md={8} sm={12} xs={12}>
                        <Col md={6} sm={12} xs={12}>
                          <IndicatorBox
                            icon="findings"
                            name={translate.t("search_findings.tab_indicators.total_findings")}
                            quantity={data.project.totalFindings}
                            title=""
                            total=""
                            onClick={goToProjectFindings}
                          />
                        </Col>
                        <Col md={6} sm={12} xs={12}>
                          <IndicatorBox
                            icon="vulnerabilities"
                            name={translate.t("search_findings.tab_indicators.total_vulnerabilitites")}
                            quantity={totalVulnerabilities}
                            title=""
                            total=""
                            onClick={goToProjectFindings}
                          />
                        </Col>
                        <Col md={6} sm={12} xs={12}>
                          <IndicatorBox
                            icon="totalVulnerabilities"
                            name={translate.t("search_findings.tab_indicators.pending_closing_check")}
                            quantity={data.project.pendingClosingCheck}
                            title=""
                            total=""
                            onClick={goToProjectFindings}
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
                            onClick={goToProjectFindings}
                          />
                        </Col>
                        <Col md={6} sm={12} xs={12}>
                          <IndicatorBox
                            icon="graph"
                            name={translate.t("search_findings.tab_indicators.mean_remediate")}
                            quantity={data.project.meanRemediate}
                            title=""
                            total={translate.t("search_findings.tab_indicators.days")}
                            onClick={goToProjectFindings}
                          />
                        </Col>
                        <Col md={6} sm={12} xs={12}>
                          <IndicatorBox
                            icon="vectorLocal"
                            name={translate.t("search_findings.tab_indicators.max_severity")}
                            quantity={data.project.maxSeverity}
                            title=""
                            total="/10"
                            onClick={goToProjectFindings}
                          />
                        </Col>
                        <Col md={6} sm={12} xs={12}>
                          <IndicatorBox
                            icon="openVulnerabilities"
                            name={translate.t("search_findings.tab_indicators.max_open_severity")}
                            quantity={data.project.maxOpenSeverity}
                            title=""
                            total="/10"
                            onClick={goToProjectFindings}
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
                        onClick={goToProjectSettings}
                      />
                    </Col>
                    <Col md={4} sm={12} xs={12}>
                      <IndicatorBox
                        icon="authors"
                        name={translate.t("search_findings.tab_indicators.authors")}
                        quantity={data.project.currentMonthAuthors}
                        title=""
                        total=""
                        onClick={goToProjectSettings}
                      />
                    </Col>
                    <Col md={4} sm={12} xs={12}>
                      <IndicatorBox
                        icon="terminal"
                        name={translate.t("search_findings.tab_indicators.commits")}
                        quantity={data.project.currentMonthCommits}
                        title=""
                        total=""
                        onClick={goToProjectSettings}
                      />
                    </Col>
                  </Col>
                </Row>
                <br />
                <br />
                <hr />
                <Row>
                  <Col md={12} sm={12} xs={12}>
                    <h1 className={style.title}>{translate.t("search_findings.tab_indicators.forces.title")}</h1>
                    <Col md={4} sm={12} xs={12}>
                      {data.project.hasForces ? (
                        <IndicatorBox
                          icon="verified"
                          name={translate.t("search_findings.tab_indicators.forces.indicators.has_forces.title")}
                          quantity={
                            translate.t("search_findings.tab_indicators.forces.indicators.has_forces.protected")}
                          onClick={goToProjectForces}
                          title=""
                          total=""
                          description={
                            translate.t("search_findings.tab_indicators.forces.indicators.has_forces.protected_desc")}
                          small={true}
                        />
                      ) : (
                        <IndicatorBox
                          icon="fail"
                          name={translate.t("search_findings.tab_indicators.forces.indicators.has_forces.title")}
                          quantity={
                            translate.t("search_findings.tab_indicators.forces.indicators.has_forces.unprotected")}
                          title=""
                          total=""
                          description={
                            translate.t("search_findings.tab_indicators.forces.indicators.has_forces.unprotected_desc")}
                          small={true}
                        />
                      )}
                    </Col>
                    <Col md={4} sm={12} xs={12}>
                      {data.project.hasForces ? (
                        <IndicatorBox
                          icon="authors"
                          name={translate.t("search_findings.tab_indicators.forces.indicators.strictness.title")}
                          quantity={securityCommitment}
                          onClick={goToProjectForces}
                          title=""
                          total={translate.t("search_findings.tab_indicators.forces.indicators.strictness.total")}
                          description={
                            translate.t("search_findings.tab_indicators.forces.indicators.strictness.strict_desc")}
                          small={true}
                        />
                      ) : (
                        <React.Fragment />
                      )}
                    </Col>
                  </Col>
                </Row>

              </React.StrictMode>
            );
          } else { return <React.Fragment />; }
        }}
    </Query>
  );
};

export { indicatorsView as ProjectIndicatorsView };
