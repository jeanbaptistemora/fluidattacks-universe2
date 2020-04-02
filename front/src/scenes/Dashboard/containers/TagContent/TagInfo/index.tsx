import { useQuery } from "@apollo/react-hooks";
import { ChartData, ChartDataSets, ChartOptions } from "chart.js";
import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router-dom";
import {
  calcPercent, IStatusGraph, ITreatmentGraph, statusGraph, treatmentGraph,
} from "../../../../../utils/formatHelpers";
import translate from "../../../../../utils/translations/translate";
import { IndicatorBox } from "../../../components/IndicatorBox";
import { IndicatorGraph } from "../../../components/IndicatorGraph";
import { IndicatorStack } from "../../../components/IndicatorStack";
import { default as style } from "./index.css";
import { TAG_QUERY } from "./queries";

type TagsProps = RouteComponentProps<{ tagName: string }>;

interface IStackedGraph {
  acceptedUndefinedVulnerabilities: number;
  acceptedVulnerabilities: number;
  closedVulnerabilities: number;
  name: string;
  openVulnerabilities: number;
}

interface IStatusGraphName extends IStatusGraph {
  name: string;
}

interface IProjectTag {
  closedVulnerabilities: number;
  lastClosingVuln: number;
  maxOpenSeverity: number;
  maxSeverity: number;
  meanRemediate: number;
  name: string;
  openVulnerabilities: number;
  totalTreatment: string;
}
interface IBoxInfo {
  name: string;
  value: number;
}
interface ITag {
  tag: {
    name: string;
    projects: IProjectTag[];
  };
}
const tagsInfo: React.FC<TagsProps> = (props: TagsProps): JSX.Element => {
  const { tagName } = props.match.params;
  const { data } = useQuery<ITag>(TAG_QUERY, { variables: { tag: tagName }});

  const formatStatusGraphData: ((projects: ITreatmentGraph[]) => IStatusGraph) = (
    projects: ITreatmentGraph[],
  ): IStatusGraph => {
    const closedVulnerabilities: number = projects.reduce(
      (acc: number, project: ITreatmentGraph) => (acc + project.closedVulnerabilities), 0);
    const openVulnerabilities: number = projects.reduce(
      (acc: number, project: ITreatmentGraph) => (acc + project.openVulnerabilities), 0);

    return { closedVulnerabilities, openVulnerabilities };
  };

  const formatTreatmentGraphData: ((projects: ITreatmentGraph[]) => ITreatmentGraph) = (
    projects: ITreatmentGraph[],
  ): ITreatmentGraph => {
    const totalTreatment: Dictionary<number> = projects.reduce(
      (acc: Dictionary<number>, project: ITreatmentGraph) => {
        const projectTreatment: Dictionary<number> = JSON.parse(project.totalTreatment);

        return ({
          accepted: acc.accepted + projectTreatment.accepted,
          acceptedUndefined: acc.accepted + projectTreatment.acceptedUndefined,
          inProgress: acc.inProgress + projectTreatment.inProgress,
          undefined: acc.undefined + projectTreatment.undefined,
        });
      },
      { accepted: 0, acceptedUndefined: 0, inProgress: 0, undefined: 0 });

    return { totalTreatment: JSON.stringify(totalTreatment), ...formatStatusGraphData(projects) };
  };

  const remediatedPercent: ((graphProps: IProjectTag) => IStatusGraphName) = (
    graphProps: IProjectTag,
  ): IStatusGraphName => {
    const { openVulnerabilities, closedVulnerabilities } = graphProps;
    const totalVulnerabilities: number = openVulnerabilities + closedVulnerabilities;
    const openPercent: number = calcPercent(openVulnerabilities, totalVulnerabilities);
    const closedPercent: number = _.round(100 - openPercent, 1);

    return { openVulnerabilities: openPercent, closedVulnerabilities: closedPercent, name: graphProps.name };
  };

  const sortRemdiatedGraph: ((aObject: IStatusGraphName, bObject: IStatusGraphName) => number) = (
    aObject: IStatusGraphName, bObject: IStatusGraphName,
  ): number => (
    aObject.closedVulnerabilities - bObject.closedVulnerabilities
  );

  const remediatedAcceptedPercent: ((graphProps: IProjectTag) => IStackedGraph) = (
    graphProps: IProjectTag,
  ): IStackedGraph => {
    const { openVulnerabilities, closedVulnerabilities } = graphProps;
    const projectTreatment: Dictionary<number> = JSON.parse(graphProps.totalTreatment);
    const totalVulnerabilities: number = openVulnerabilities + closedVulnerabilities;
    const openPercent: number = calcPercent(
      openVulnerabilities - projectTreatment.accepted - projectTreatment.acceptedUndefined, totalVulnerabilities);
    const acceptedPercent: number = calcPercent(projectTreatment.accepted, totalVulnerabilities);
    const closedPercent: number = calcPercent(closedVulnerabilities, totalVulnerabilities);
    const acceptedUndefinedPercent: number = _.round(100 - acceptedPercent - openPercent - closedPercent, 1);

    return {
      acceptedUndefinedVulnerabilities: acceptedUndefinedPercent,
      acceptedVulnerabilities: acceptedPercent,
      closedVulnerabilities: closedPercent,
      name: graphProps.name,
      openVulnerabilities: openPercent,
    };
  };

  const formatRemediatedAcceptedVuln: ((projects: IProjectTag[]) => ChartData) = (
    projects: IProjectTag[],
  ): ChartData => {
    const dataPercent: IStackedGraph[] = projects.map(remediatedAcceptedPercent);
    const dataPercentSorted: IStackedGraph[] = dataPercent.sort(sortRemdiatedGraph);
    const statusDataset: ChartDataSets[] = [
      {
        backgroundColor: "#27BF4F",
        data: dataPercentSorted.map((projectPercent: IStackedGraph) => projectPercent.closedVulnerabilities),
        hoverBackgroundColor: "#069D2E",
        label: `% ${translate.t("search_findings.tab_indicators.closed")}`,
        stack: "4",
      },
      {
        backgroundColor: "#b7b7b7",
        data: dataPercentSorted.map((projectPercent: IStackedGraph) => projectPercent.acceptedVulnerabilities),
        hoverBackgroundColor: "#999797",
        label: `% ${translate.t("search_findings.tab_indicators.treatment_accepted")}`,
        stack: "4",
      },
      {
        backgroundColor: "#000",
        data: dataPercentSorted.map((projectPercent: IStackedGraph) => projectPercent.acceptedUndefinedVulnerabilities),
        hoverBackgroundColor: "#000",
        label: `% ${translate.t("search_findings.tab_indicators.treatment_accepted_undefined")}`,
        stack: "4",
      },
      {
        backgroundColor: "#ff1a1a",
        data: dataPercentSorted.map((projectPercent: IStackedGraph) => projectPercent.openVulnerabilities),
        hoverBackgroundColor: "#e51414",
        label: `% ${translate.t("search_findings.tab_indicators.open")}`,
        stack: "4",
      },
    ];
    const stackedBarGraphData: ChartData = {
      datasets: statusDataset,
      labels: dataPercentSorted.map((project: IStackedGraph) => project.name),
    };

    return stackedBarGraphData;
  };

  const formatRemediatedVuln: ((projects: IProjectTag[]) => ChartData) = (projects: IProjectTag[]): ChartData => {
    const dataPercent: IStatusGraphName[] = projects.map(remediatedPercent);
    const dataPercentSorted: IStatusGraphName[] = dataPercent.sort(sortRemdiatedGraph);
    const statusDataset: Array<Dictionary<string | number []>> = [
      {
        backgroundColor: "#27BF4F",
        data: dataPercentSorted.map((projectPercent: IStatusGraph) => projectPercent.closedVulnerabilities),
        hoverBackgroundColor: "#069D2E",
        label: `% ${translate.t("search_findings.tab_indicators.closed")}`,
        stack: "2",
      },
      {
        backgroundColor: "#ff1a1a",
        data: dataPercentSorted.map((projectPercent: IStatusGraph) => projectPercent.openVulnerabilities),
        hoverBackgroundColor: "#e51414",
        label: `% ${translate.t("search_findings.tab_indicators.open")}`,
        stack: "2",
      },
    ];
    const stackedBarGraphData: Dictionary<string[] | Array<Dictionary<string | number []>>> = {
      datasets: statusDataset,
      labels: dataPercentSorted.map((project: IStatusGraphName) => project.name),
    };

    return stackedBarGraphData;
  };

  const yAxesLabel: ((value: number) => string | number) = (value: number): string | number => (
    value % 20 === 0 ? value : ""
  );

  const chartOptions: ChartOptions = {
    legend: { display: true, position: "top" },
    scales: {
      xAxes: [{ stacked: true, gridLines: { display: false }, ticks: { autoSkip: false } }],
      yAxes: [{ stacked: true, gridLines: { display: false }, ticks: { callback: yAxesLabel } }],
    },
  };

  const calculateMeanToRemediate: ((projects: IProjectTag[]) => number) = (projects: IProjectTag[]): number => (
    Math.ceil(
      projects.reduce((acc: number, project: IProjectTag) => acc + project.meanRemediate, 0) / projects.length)
  );

  const getMaxSeverity: ((projects: IProjectTag[]) => IBoxInfo) = (projects: IProjectTag[]): IBoxInfo => {
    let projectName: string = "";
    const maxFound: number = projects.reduce(
      (maxValue: number, project: IProjectTag) => {
        let max: number = maxValue;
        if (project.maxSeverity > maxValue) {
          max = project.maxSeverity;
          projectName = project.name;
        }

        return max;
      },
      0);

    return { name: projectName, value: maxFound };
  };

  const getMaxOpenSeverity: ((projects: IProjectTag[]) => IBoxInfo) = (projects: IProjectTag[]): IBoxInfo => {
    let projectName: string = "";
    const maxOpen: number = projects.reduce(
      (maxValue: number, project: IProjectTag) => {
        let max: number = maxValue;
        if (project.maxOpenSeverity > maxValue) {
          max = project.maxOpenSeverity;
          projectName = project.name;
        }

        return max;
      },
      0);

    return { name: projectName, value: maxOpen };
  };

  const getLastClosingVuln: ((projects: IProjectTag[]) => number) = (projects: IProjectTag[]): number => (
    projects.reduce(
      (maxValue: number, project: IProjectTag) => project.lastClosingVuln < maxValue ?
        project.lastClosingVuln : maxValue,
      Number.MAX_SAFE_INTEGER)
  );

  if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

  const goToProjectMaxSeverityFindings: (() => void) = (): void => {
    location.hash = `#!/project/${getMaxSeverity(data.tag.projects).name}/findings`;
  };
  const goToProjectMaxOpenSeverityFindings: (() => void) = (): void => {
    location.hash = `#!/project/${getMaxOpenSeverity(data.tag.projects).name}/findings`;
  };
  const projectWithMaxSeverity: IBoxInfo = getMaxSeverity(data.tag.projects);
  const projectWithMaxOpenSeverity: IBoxInfo = getMaxOpenSeverity(data.tag.projects);

  return (
    <React.Fragment>
      <Row>
        <Col md={3} sm={12} xs={12}>
          <IndicatorBox
            icon="graph"
            name={translate.t("search_findings.tab_indicators.mean_remediate")}
            quantity={calculateMeanToRemediate(data.tag.projects)}
            title=""
            total={translate.t("search_findings.tab_indicators.days")}
          />
        </Col>
        <Col md={3} sm={12} xs={12}>
          <IndicatorBox
            icon="vectorLocal"
            name={translate.t("search_findings.tab_indicators.max_severity")}
            quantity={projectWithMaxSeverity.value}
            title=""
            total="/10"
            description={projectWithMaxSeverity.name}
            small={true}
            onClick={goToProjectMaxSeverityFindings}
          />
        </Col>
        <Col md={3} sm={12} xs={12}>
          <IndicatorBox
            icon="openVulnerabilities"
            name={translate.t("search_findings.tab_indicators.max_open_severity")}
            quantity={projectWithMaxOpenSeverity.value}
            title=""
            total="/10"
            description={projectWithMaxOpenSeverity.name}
            small={true}
            onClick={goToProjectMaxOpenSeverityFindings}
          />
        </Col>
        <Col md={3} sm={12} xs={12}>
          <IndicatorBox
            icon="calendar"
            name={translate.t("search_findings.tab_indicators.last_closing_vuln")}
            quantity={getLastClosingVuln(data.tag.projects)}
            title=""
            total=""
          />
        </Col>
      </Row>
      <br />
      <Row>
        <Col mdOffset={1} md={10} sm={12} xs={12}>
          <IndicatorStack
            data={formatRemediatedVuln(data.tag.projects)}
            height={100}
            name={translate.t("tag_indicator.remediated_vuln")}
            options={chartOptions}
          />
        </Col>
      </Row>
      <br />
      <Row>
        <Col mdOffset={1} md={10} sm={12} xs={12}>
          <IndicatorStack
            data={formatRemediatedAcceptedVuln(data.tag.projects)}
            height={100}
            name={translate.t("tag_indicator.remediated_accepted_vuln")}
            options={chartOptions}
          />
        </Col>
      </Row>
      <br />
      <Row>
        <Col md={6} sm={12} xs={12}>
          <Col md={12} sm={12} xs={12} className={style.box_size}>
            <IndicatorGraph
              data={statusGraph(formatStatusGraphData(data.tag.projects))}
              name={translate.t("search_findings.tab_indicators.status_graph")}
            />
          </Col>
        </Col>
        <Col md={6} sm={12} xs={12}>
          <Col md={12} sm={12} xs={12} className={style.box_size}>
            <IndicatorGraph
              data={treatmentGraph(formatTreatmentGraphData(data.tag.projects))}
              name={translate.t("search_findings.tab_indicators.treatment_graph")}
            />
          </Col>
        </Col>
      </Row>
    </React.Fragment>
  );
};

export { tagsInfo as TagsInfo };
