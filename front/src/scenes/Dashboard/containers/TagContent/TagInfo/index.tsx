/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that renders indicators
 */
import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { ChartData, ChartDataSets, ChartOptions } from "chart.js";
/* tslint:disable-next-line: no-import-side-effect
 * Disabling this rule is necessary because the module attach itself
 * as a plugin to chart
 */
import "chartjs-plugin-doughnutlabel";
import _ from "lodash";
import React from "react";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { RouteComponentProps, useHistory } from "react-router-dom";
import { DataTableNext } from "../../../../../components/DataTableNext";
import { IHeader } from "../../../../../components/DataTableNext/types";
import { default as globalStyle } from "../../../../../styles/global.css";
import {
  calcPercent, IStatusGraph, ITreatmentGraph, statusGraph, treatmentGraph,
} from "../../../../../utils/formatHelpers";
import { msgError } from "../../../../../utils/notifications";
import rollbar from "../../../../../utils/rollbar";
import translate from "../../../../../utils/translations/translate";
import { HorizontalBarIndicator } from "../../../components/HorizontalBarIndicator";
import { IndicatorBox } from "../../../components/IndicatorBox";
import { IndicatorGraph } from "../../../components/IndicatorGraph";
import { IndicatorStack } from "../../../components/IndicatorStack";
import { IFindingAttr } from "../../ProjectFindingsView/types";
import { default as style } from "./index.css";
import { TAG_QUERY } from "./queries";

export type TagsProps = RouteComponentProps<{ tagName: string }>;

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
  description: string;
  lastClosingVuln: number;
  lastClosingVulnFinding: IFindingAttr;
  maxOpenSeverity: number;
  maxSeverity: number;
  name: string;
  openFindings: number;
  openVulnerabilities: number;
  totalFindings: number;
  totalTreatment: string;
}
interface IBoxInfo {
  name: string;
  value: number;
}
interface ITag {
  tag: {
    lastClosingVuln: number;
    maxOpenSeverity: number;
    maxSeverity: number;
    meanRemediate: number;
    meanRemediateCriticalSeverity: number;
    meanRemediateHighSeverity: number;
    meanRemediateLowSeverity: number;
    meanRemediateMediumSeverity: number;
    name: string;
    projects: IProjectTag[];
  };
}
interface IProjectTable {
  description: string;
  name: string;
}
const maxNumberOfDisplayedProjects: number = 6;

const tagsInfo: React.FC<TagsProps> = (props: TagsProps): JSX.Element => {
  const { tagName } = props.match.params;
  const { data } = useQuery<ITag>(TAG_QUERY, {
    onError: (error: ApolloError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      rollbar.error("An error occurred loading tag info", error);
    },
    variables: { tag: tagName },
  });
  const { push } = useHistory();

  const tableHeaders: IHeader[] = [
    { dataField: "name", header: "Project Name" },
    { dataField: "description", header: "Description" },
  ];

  const handleRowTagClick: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string }) => void) = (
    _0: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string },
  ): void => {
    push(`/groups/${rowInfo.name.toLowerCase()}/indicators`);
  };

  const formatTableData: ((projects: IProjectTag[]) => IProjectTable[]) = (
    projects: IProjectTag[],
  ): IProjectTable[] => (
    projects.map((project: IProjectTag) => ({ name: project.name, description: project.description }))
  );

  const formatStatusGraphData: ((projects: ITreatmentGraph[]) => IStatusGraph) = (
    projects: ITreatmentGraph[],
  ): IStatusGraph => {
    const closedVulnerabilities: number = projects.reduce(
      (acc: number, project: ITreatmentGraph) => (acc + project.closedVulnerabilities), 0);
    const openVulnerabilities: number = projects.reduce(
      (acc: number, project: ITreatmentGraph) => (acc + project.openVulnerabilities), 0);

    return { closedVulnerabilities, openVulnerabilities };
  };

  const getNumberOfVulns: ((projects: ITreatmentGraph[]) => number) = (
    projects: ITreatmentGraph[],
  ): number => {
    const { closedVulnerabilities, openVulnerabilities } = formatStatusGraphData(projects);

    return closedVulnerabilities + openVulnerabilities;
  };

  const getNumberOfUndefinedVulns: ((projects: IProjectTag[]) => number) = (projects: IProjectTag[]): number => (
    projects.reduce(
      (acc: number, project: IProjectTag) => {
        const projectTreatment: Dictionary<number> = JSON.parse(project.totalTreatment);

        return acc + projectTreatment.undefined;
      },
      0)
  );

  const getNumberOfOpenVulns: ((projects: ITreatmentGraph[]) => number) = (
    projects: ITreatmentGraph[],
  ): number => (
    projects.reduce((acc: number, project: ITreatmentGraph) => (acc + project.openVulnerabilities), 0)
  );

  const formatTreatmentGraphData: ((projects: ITreatmentGraph[]) => ITreatmentGraph) = (
    projects: ITreatmentGraph[],
  ): ITreatmentGraph => {
    const totalTreatment: Dictionary<number> = projects.reduce(
      (acc: Dictionary<number>, project: ITreatmentGraph) => {
        const projectTreatment: Dictionary<number> = JSON.parse(project.totalTreatment);

        return ({
          accepted: acc.accepted + projectTreatment.accepted,
          acceptedUndefined: acc.acceptedUndefined + projectTreatment.acceptedUndefined,
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

  const horizontalBarOptions: ChartOptions = {
    legend: { display: false },
    scales: {
      xAxes: [{ gridLines: { display: false } }],
      yAxes: [{ gridLines: { display: false } }],
    },
  };

  const formatMeanRemediated: ((tag: ITag["tag"]) => ChartData) = (tag: ITag["tag"]): ChartData => {
    const statusDataset: ChartDataSets = {
      backgroundColor: "#0b84a5",
      data: [
        _.round(tag.meanRemediateCriticalSeverity, 1), _.round(tag.meanRemediateHighSeverity, 1),
        _.round(tag.meanRemediateMediumSeverity, 1), _.round(tag.meanRemediateLowSeverity, 1),
      ],
    };
    const barData: ChartData = {
      datasets: [statusDataset],
      labels: [
        translate.t("tag_indicator.critical_severity"), translate.t("tag_indicator.high_severity"),
        translate.t("tag_indicator.medium_severity"), translate.t("tag_indicator.low_severity"),
      ],
    };

    return barData;
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

  const formatYAxesBarLabel: ((value: number) => string | number) = (value: number): string | number => (
    Math.floor(value) === value ? value : ""
  );

  const sortByOpenFindings: ((projectA: IProjectTag, projectB: IProjectTag) => number) = (
    projectA: IProjectTag, projectB: IProjectTag,
  ): number => (
    projectB.openFindings - projectA.openFindings
  );

  const formatOpenFindings: ((projects: IProjectTag[]) => ChartData) = (projects: IProjectTag[]): ChartData => {
    const sortedProjects: IProjectTag[] = projects.sort(sortByOpenFindings);
    const statusDataset: ChartDataSets = {
      backgroundColor: "#0b84a5",
      data: sortedProjects.map((project: IProjectTag) => project.openFindings),
      pointRadius: 1,
    };
    const barData: ChartData = {
      datasets: [statusDataset],
      labels: sortedProjects.map((project: IProjectTag) => project.name),
    };

    return barData;
  };

  const chartBarOptions: ChartOptions = {
    legend: { display: false },
    scales: {
      xAxes: [{ gridLines: { display: false }, ticks: { autoSkip: false } }],
      yAxes: [{ gridLines: { display: false }, ticks: { beginAtZero: true, callback: formatYAxesBarLabel } }],
    },
  };

  const sortByTotalFindings: ((projectA: IProjectTag, projectB: IProjectTag) => number) = (
    projectA: IProjectTag, projectB: IProjectTag,
  ): number => (
    projectB.totalFindings - projectA.totalFindings
  );

  const formatTotalFindings: ((projects: IProjectTag[]) => ChartData) = (projects: IProjectTag[]): ChartData => {
    const sortedProjects: IProjectTag[] = projects.sort(sortByTotalFindings);
    const statusDataset: ChartDataSets = {
      backgroundColor: "#0b84a5",
      data: sortedProjects.map((project: IProjectTag) => project.totalFindings),
    };
    const barData: ChartData = {
      datasets: [statusDataset],
      labels: sortedProjects.map((project: IProjectTag) => project.name),
    };

    return barData;
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

  const formatDoughnutOptions: ((numberOfVulns: number, smallLabel: string) => ChartOptions) = (
    numberOfVulns: number, smallLabel: string,
  ): ChartOptions => ({
    plugins: {
      doughnutlabel: {
        labels: [
          {
            color: "#000",
            font: { size: "50", weight: "bold" },
            text: numberOfVulns,
          },
          {
            color: "#000",
            font: { size: "20" },
            text: smallLabel,
          },
        ],
      },
    },
  });

  const getMaxSeverityProject: ((projects: IProjectTag[]) => string) = (projects: IProjectTag[]): string => (
    projects.reduce(
      (maxValue: IProjectTag, project: IProjectTag) =>
        (project.maxSeverity > maxValue.maxSeverity ? project : maxValue),
      projects[0]).name
  );

  const getMaxOpenSeverityProject: ((projects: IProjectTag[]) => string) = (projects: IProjectTag[]): string => (
    projects.reduce(
      (maxValue: IProjectTag, project: IProjectTag) =>
        (project.maxOpenSeverity > maxValue.maxOpenSeverity ? project : maxValue),
      projects[0]).name
  );

  const getLastClosingVulnProject: ((projects: IProjectTag[]) => string) = (projects: IProjectTag[]): string => (
    projects.reduce(
      (maxValue: IProjectTag, project: IProjectTag) =>
        (project.lastClosingVuln < maxValue.lastClosingVuln ? project : maxValue),
      projects[0]).name
  );

  const getLastClosingVulnFindingId: ((projects: IProjectTag[]) => string) = (projects: IProjectTag[]): string => (
    projects.reduce(
      (maxValue: IProjectTag, project: IProjectTag) =>
        (project.lastClosingVuln < maxValue.lastClosingVuln ? project : maxValue),
      projects[0]).lastClosingVulnFinding.id
  );

  const sortBoxInfo: ((aObject: IBoxInfo, bObject: IBoxInfo) => number) = (
    aObject: IBoxInfo, bObject: IBoxInfo,
  ): number => (
    bObject.value - aObject.value
  );

  const getPercentUndefinedVulnerabilities: ((project: IProjectTag) => IBoxInfo) = (
    project: IProjectTag,
  ): IBoxInfo => {
    const projectTreatment: Dictionary<number> = JSON.parse(project.totalTreatment);

    return { value: projectTreatment.undefined, name: project.name };
  };

  const getTotalVulnsByProject: ((project: IProjectTag) => IBoxInfo) = (
    project: IProjectTag,
  ): IBoxInfo => (
    ({ value: project.openVulnerabilities + project.closedVulnerabilities, name: project.name })
  );

  const getRandomColor: ((projects: string[]) => Dictionary<string>) = (projects: string[]): Dictionary<string> => (
    Object.assign({}, ...projects.map((project: string) => ({
      [`${project}`]:
        `${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}`,
    })))
  );

  const customDoughnutBorder: ChartDataSets = {
    borderWidth: 0, hoverBorderWidth: 2,
  };

  const formatUndefinedGraph: ((projects: IProjectTag[], colors: Dictionary<string>) => ChartData) = (
    projects: IProjectTag[], colors: Dictionary<string>,
  ): ChartData => {
    const totalUndefinedVulnerabilities: number = getNumberOfUndefinedVulns(projects);
    const dataGraphs: IBoxInfo[] = projects.map(getPercentUndefinedVulnerabilities);
    const dataGraphSorted: IBoxInfo[] = dataGraphs.sort(sortBoxInfo);
    let dataGraphSortedSliced: IBoxInfo[] = dataGraphSorted.slice(0, maxNumberOfDisplayedProjects);
    const remainingVulns: number = totalUndefinedVulnerabilities - dataGraphSortedSliced.reduce(
      (acc: number, dataGraph: IBoxInfo) => acc + dataGraph.value, 0);
    dataGraphSortedSliced = remainingVulns > 0 ?
      [...dataGraphSortedSliced, {name: translate.t("home.tagOther"), value: remainingVulns}] : dataGraphSortedSliced;
    const chartData: ChartData = {
      datasets: [{
        backgroundColor: dataGraphSortedSliced.map((dataGraph: IBoxInfo) => `rgb(${colors[dataGraph.name]}, 0.75)`),
        data: dataGraphSortedSliced.map((dataGraph: IBoxInfo) => dataGraph.value),
        hoverBackgroundColor: dataGraphSortedSliced.map((dataGraph: IBoxInfo) => `rgb(${colors[dataGraph.name]}, 1)`),
        ...customDoughnutBorder,
      }],
      labels: dataGraphSortedSliced.map(
        (dataGraph: IBoxInfo) => `${calcPercent(dataGraph.value, totalUndefinedVulnerabilities)}% ${dataGraph.name}`),
    };

    return chartData;
  };

  const formatVulnsGraph: ((projects: IProjectTag[], colors: Dictionary<string>) => ChartData) = (
    projects: IProjectTag[], colors: Dictionary<string>,
  ): ChartData => {
    const totalVulnerabilities: number = getNumberOfVulns(projects);
    const dataGraphs: IBoxInfo[] = projects.map(getTotalVulnsByProject);
    const dataGraphSorted: IBoxInfo[] = dataGraphs.sort(sortBoxInfo);
    let dataGraphSortedSliced: IBoxInfo[] = dataGraphSorted.slice(0, maxNumberOfDisplayedProjects);
    const remainingVulns: number = totalVulnerabilities - dataGraphSortedSliced.reduce(
      (acc: number, dataGraph: IBoxInfo) => acc + dataGraph.value, 0);
    dataGraphSortedSliced = remainingVulns > 0 ?
      [...dataGraphSortedSliced, {name: translate.t("home.tagOther"), value: remainingVulns}] : dataGraphSortedSliced;
    const chartData: ChartData = {
      datasets: [{
        backgroundColor: dataGraphSortedSliced.map((dataGraph: IBoxInfo) => `rgb(${colors[dataGraph.name]}, 0.75)`),
        data: dataGraphSortedSliced.map((dataGraph: IBoxInfo) => dataGraph.value),
        hoverBackgroundColor: dataGraphSortedSliced.map((dataGraph: IBoxInfo) => `rgb(${colors[dataGraph.name]}, 1)`),
        ...customDoughnutBorder,
      }],
      labels: dataGraphSortedSliced.map(
        (dataGraph: IBoxInfo) => `${calcPercent(dataGraph.value, totalVulnerabilities)}% ${dataGraph.name}`),
    };

    return chartData;
  };

  const formatOpenVulnsGraph: ((projects: IProjectTag[], colors: Dictionary<string>) => ChartData) = (
    projects: IProjectTag[], colors: Dictionary<string>,
  ): ChartData => {
    const totalVulnerabilities: number = getNumberOfOpenVulns(projects);
    const dataGraphs: IBoxInfo[] = projects.map(
      (project: IProjectTag) => ({ value: project.openVulnerabilities, name: project.name }));
    const dataGraphSorted: IBoxInfo[] = dataGraphs.sort(sortBoxInfo);
    let dataGraphSortedSliced: IBoxInfo[] = dataGraphSorted.slice(0, maxNumberOfDisplayedProjects);
    const remainingVulns: number = totalVulnerabilities - dataGraphSortedSliced.reduce(
      (acc: number, dataGraph: IBoxInfo) => acc + dataGraph.value, 0);
    dataGraphSortedSliced = remainingVulns > 0 ?
      [...dataGraphSortedSliced, {name: translate.t("home.tagOther"), value: remainingVulns}] : dataGraphSortedSliced;
    const chartData: ChartData = {
      datasets: [{
        backgroundColor: dataGraphSortedSliced.map((dataGraph: IBoxInfo) => `rgb(${colors[dataGraph.name]}, 0.75)`),
        data: dataGraphSortedSliced.map((dataGraph: IBoxInfo) => dataGraph.value),
        hoverBackgroundColor: dataGraphSortedSliced.map((dataGraph: IBoxInfo) => `rgb(${colors[dataGraph.name]}, 1)`),
        ...customDoughnutBorder,
      }],
      labels: dataGraphSortedSliced.map(
        (dataGraph: IBoxInfo) => `${calcPercent(dataGraph.value, totalVulnerabilities)}% ${dataGraph.name}`),
    };

    return chartData;
  };

  const chartGraphOptions: ChartOptions = {
    legend: { labels: { padding: 6, usePointStyle: true } },
  };

  if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

  if (_.isEmpty(data.tag.projects)) {
    return (
      <Row>
        <div className={globalStyle.noData}>
          <Glyphicon glyph="list" />
          <p>{translate.t("dataTableNext.noDataIndication")}</p>
        </div>
      </Row>
    );
  }

  const randomColors: Dictionary<string> = getRandomColor(
    [...data.tag.projects.map((project: IProjectTag) => project.name), translate.t("home.tagOther")]);
  const projectWithMaxSeverity: string = getMaxSeverityProject(data.tag.projects);
  const projectWithMaxOpenSeverity: string = getMaxOpenSeverityProject(data.tag.projects);
  const projectWithLastClosingVuln: string = getLastClosingVulnProject(data.tag.projects);
  const findingIdWithLastClosingVuln: string = getLastClosingVulnFindingId(data.tag.projects);
  const goToProjectMaxSeverityFindings: (() => void) = (): void => {
    push(`/groups/${projectWithMaxSeverity.toLowerCase()}/findings`);
  };
  const goToProjectMaxOpenSeverityFindings: (() => void) = (): void => {
    push(`/groups/${projectWithMaxOpenSeverity.toLowerCase()}/findings`);
  };
  const goToProjectFindingTracking: (() => void) = (): void => {
    push(`/groups/${projectWithLastClosingVuln.toLowerCase()}/findings/${findingIdWithLastClosingVuln}/tracking`);
  };

  return (
    <React.Fragment>
      <Row>
        <DataTableNext
          bordered={true}
          dataset={formatTableData(data.tag.projects)}
          exportCsv={false}
          headers={tableHeaders}
          id="tblProjectsTag"
          pageSize={10}
          remote={false}
          rowEvents={{ onClick: handleRowTagClick }}
          search={true}
        />
      </Row>
      <Row>
        <Col md={3} sm={12} xs={12}>
          <IndicatorBox
            icon="graph"
            name={translate.t("search_findings.tab_indicators.mean_remediate")}
            quantity={_.round(data.tag.meanRemediate, 1)}
            title=""
            total={translate.t("search_findings.tab_indicators.days")}
          />
        </Col>
        <Col md={3} sm={12} xs={12}>
          <IndicatorBox
            icon="vectorLocal"
            name={translate.t("search_findings.tab_indicators.max_severity")}
            quantity={_.round(data.tag.maxSeverity, 1)}
            title=""
            total="/10"
            small={true}
            description={projectWithMaxSeverity.toLowerCase()}
            onClick={goToProjectMaxSeverityFindings}
          />
        </Col>
        <Col md={3} sm={12} xs={12}>
          <IndicatorBox
            icon="openVulnerabilities"
            name={translate.t("search_findings.tab_indicators.max_open_severity")}
            quantity={_.round(data.tag.maxOpenSeverity, 1)}
            title=""
            total="/10"
            small={true}
            description={projectWithMaxOpenSeverity.toLowerCase()}
            onClick={goToProjectMaxOpenSeverityFindings}
          />
        </Col>
        <Col md={3} sm={12} xs={12}>
          <IndicatorBox
            icon="calendar"
            name={translate.t("search_findings.tab_indicators.last_closing_vuln")}
            quantity={_.round(data.tag.lastClosingVuln, 1)}
            title=""
            total=""
            small={true}
            description={projectWithLastClosingVuln.toLowerCase()}
            onClick={goToProjectFindingTracking}
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
        <Col mdOffset={1} md={10} sm={12} xs={12}>
          <IndicatorStack
            data={formatTotalFindings(data.tag.projects)}
            height={100}
            name={translate.t("tag_indicator.findings_group")}
            options={chartBarOptions}
          />
        </Col>
      </Row>
      <br />
      <Row>
        <Col mdOffset={1} md={10} sm={12} xs={12}>
          <IndicatorStack
            data={formatOpenFindings(data.tag.projects)}
            height={100}
            name={translate.t("tag_indicator.open_findings_group")}
            options={chartBarOptions}
          />
        </Col>
      </Row>
      <Row>
        <Col md={6} sm={12} xs={12}>
          <IndicatorGraph
            chartClass={style.box_size}
            data={statusGraph(formatStatusGraphData(data.tag.projects))}
            name={translate.t("search_findings.tab_indicators.status_graph")}
            options={
              formatDoughnutOptions(getNumberOfVulns(data.tag.projects), translate.t("tag_indicator.total_vuln"))
            }
          />
        </Col>
        <Col md={6} sm={12} xs={12}>
          <IndicatorGraph
            chartClass={style.box_size}
            data={treatmentGraph(formatTreatmentGraphData(data.tag.projects))}
            name={translate.t("search_findings.tab_indicators.treatment_graph")}
            options={
              formatDoughnutOptions(getNumberOfOpenVulns(data.tag.projects), translate.t("tag_indicator.open_vuln"))
            }
          />
        </Col>
      </Row>
      <br />
      <Row>
        <Col md={6} sm={12} xs={12}>
          <HorizontalBarIndicator
            data={formatMeanRemediated(data.tag)}
            height={200}
            name={translate.t("tag_indicator.mean_remediate")}
            options={horizontalBarOptions}
          />
        </Col>
        <Col md={6} sm={12} xs={12}>
          <IndicatorGraph
            chartClass={style.box_size}
            data={formatUndefinedGraph(data.tag.projects, randomColors)}
            name={translate.t("tag_indicator.undefined_title")}
            options={{
              ...chartGraphOptions,
              ...formatDoughnutOptions(
                getNumberOfUndefinedVulns(data.tag.projects), translate.t("tag_indicator.undefined_vuln"),
              ),
            }}
          />
        </Col>
      </Row>
      <br />
      <Row>
        <Col md={6} sm={12} xs={12}>
          <IndicatorGraph
            chartClass={style.box_size}
            data={formatVulnsGraph(data.tag.projects, randomColors)}
            name={translate.t("tag_indicator.vulns_groups")}
            options={{
              ...chartGraphOptions,
              ...formatDoughnutOptions(
                getNumberOfVulns(data.tag.projects), translate.t("tag_indicator.total_vuln"),
              ),
            }}
          />
        </Col>
        <Col md={6} sm={12} xs={12}>
          <IndicatorGraph
            chartClass={style.box_size}
            data={formatOpenVulnsGraph(data.tag.projects, randomColors)}
            name={translate.t("tag_indicator.open_vulns_groups")}
            options={{
              ...chartGraphOptions,
              ...formatDoughnutOptions(
                getNumberOfOpenVulns(data.tag.projects), translate.t("tag_indicator.open_vuln"),
              ),
            }}
          />
        </Col>
      </Row>
    </React.Fragment>
  );
};

export { tagsInfo as TagsInfo };
