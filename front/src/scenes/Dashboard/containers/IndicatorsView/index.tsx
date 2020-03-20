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
import { calcPercent, handleGraphQLErrors, IGraphData, statusGraph } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { IndicatorBox } from "../../components/IndicatorBox/index";
import { IndicatorChart } from "../../components/IndicatorChart";
import { IndicatorGraph } from "../../components/IndicatorGraph/index";
import { ForcesIndicatorsView } from "../ForcesIndicatorsView/index";
import { IRepositoriesAttr } from "../ProjectSettingsView/types";
import { default as style } from "./index.css";
import { GET_INDICATORS } from "./queries";
import { IIndicatorsProps, IIndicatorsViewBaseProps } from "./types";

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
            const activeRepositories: IRepositoriesAttr[] = JSON.parse(data.resources.repositories)
              .filter((repo: IRepositoriesAttr) =>
              !("historic_state" in repo) ||
              repo.historic_state[repo.historic_state.length - 1].state === "ACTIVE");

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
                        quantity={activeRepositories.length}
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
                <ForcesIndicatorsView projectName={projectName} />
              </React.StrictMode>
            );
          } else { return <React.Fragment />; }
        }}
    </Query>
  );
};

export { indicatorsView as ProjectIndicatorsView };
