import _ from "lodash";
import React from "react";
import { Col, Grid, Panel, Row } from "react-bootstrap";
import { Graphic } from "../../../../graphics/components/Graphic";
import translate from "../../../../utils/translations/translate";
import { ChartsGenericViewExtras } from "./components/Extras";
import styles from "./index.css";
import { EntityType, IChartsGenericViewProps } from "./types";

const chartsGenericView: React.FC<IChartsGenericViewProps> = (props: IChartsGenericViewProps): JSX.Element => {
  const { entity, reportMode, subject } = props;

  const [isForcesDescriptionExpanded, setIsForcesDescriptionExpanded] = React.useState(reportMode);

  const forcesPanelOnEnter: () => void = (): void => {
    setIsForcesDescriptionExpanded(true);
  };

  const forcesPanelOnLeave: () => void = (): void => {
    setIsForcesDescriptionExpanded(reportMode);
  };

  const doesEntityMatch: (...entities: EntityType[]) => boolean =
    (...entities: EntityType[]) => entities.includes(entity);

  return (
    <React.StrictMode>
      <Grid fluid={true}>
        {doesEntityMatch("group", "organization") ? (
          <React.Fragment>
            <Row>
              <Col md={12}>
                <Graphic
                  bsHeight={320}
                  documentName="riskOverTime"
                  documentType="stackedBarChart"
                  entity={entity}
                  footer={
                    <React.Fragment>
                      <p>{translate.t("analytics.stackedBarChart.riskOverTime.footer.intro")}</p>
                      <ul>
                        <li>{translate.t("analytics.stackedBarChart.riskOverTime.footer.opened")}</li>
                        <li>{translate.t("analytics.stackedBarChart.riskOverTime.footer.accepted")}</li>
                        <li>{translate.t("analytics.stackedBarChart.riskOverTime.footer.closed")}</li>
                      </ul>
                    </React.Fragment>
                  }
                  generatorName="generic"
                  generatorType="c3"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.stackedBarChart.riskOverTime.title")}
                />
              </Col>
            </Row>
          </React.Fragment>
        ) : undefined}
        {doesEntityMatch("group") ? (
          <React.Fragment>
            <Row>
              <Col md={6}>
                <Graphic
                  bsHeight={160}
                  documentName="status"
                  documentType="pieChart"
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.pieChart.status.footer.intro")}</p>
                  }
                  generatorName="generic"
                  generatorType="c3"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.pieChart.status.title")}
                />
              </Col>
              <Col md={6}>
                <Graphic
                  bsHeight={160}
                  documentName="treatment"
                  documentType="pieChart"
                  entity={entity}
                  footer={
                    <React.Fragment>
                      <p>{translate.t("analytics.pieChart.treatment.footer.intro")}</p>
                      <ul>
                        <li>{translate.t("analytics.pieChart.treatment.footer.notDefined")}</li>
                        <li>{translate.t("analytics.pieChart.treatment.footer.inProgress")}</li>
                        <li>{translate.t("analytics.pieChart.treatment.footer.accepted")}</li>
                        <li>{translate.t("analytics.pieChart.treatment.footer.eternally")}</li>
                      </ul>
                    </React.Fragment>
                  }
                  generatorName="generic"
                  generatorType="c3"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.pieChart.treatment.title")}
                />
              </Col>
            </Row>
            <Row>
              <Col md={4}>
                <Graphic
                  bsHeight={80}
                  documentName="totalFindings"
                  documentType="textBox"
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.textBox.totalFindings.footer")}</p>
                  }
                  generatorName="raw"
                  generatorType="textBox"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.totalFindings.title")}
                />
              </Col>
              <Col md={4}>
                <Graphic
                  bsHeight={80}
                  documentName="totalVulnerabilities"
                  documentType="textBox"
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.textBox.totalVulnerabilities.footer")}</p>
                  }
                  generatorName="raw"
                  generatorType="textBox"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.totalVulnerabilities.title")}
                />
              </Col>
              <Col md={4}>
                <Graphic
                  bsHeight={80}
                  documentName="vulnsWithUndefinedTreatment"
                  documentType="textBox"
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.textBox.vulnsWithUndefinedTreatment.footer")}</p>
                  }
                  generatorName="raw"
                  generatorType="textBox"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.vulnsWithUndefinedTreatment.title")}
                />
              </Col>
            </Row>
            <Row>
              <Col md={4}>
                <Graphic
                  bsHeight={80}
                  documentName="findingsBeingReattacked"
                  documentType="textBox"
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.textBox.findingsBeingReattacked.footer")}</p>
                  }
                  generatorName="raw"
                  generatorType="textBox"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.findingsBeingReattacked.title")}
                />
              </Col>
              <Col md={4}>
                <Graphic
                  bsHeight={80}
                  documentName="daysSinceLastRemediation"
                  documentType="textBox"
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.textBox.daysSinceLastRemediation.footer")}</p>
                  }
                  generatorName="raw"
                  generatorType="textBox"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.daysSinceLastRemediation.title")}
                />
              </Col>
              <Col md={4}>
                <Graphic
                  bsHeight={80}
                  documentName="meanTimeToRemediate"
                  documentType="textBox"
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.textBox.meanTimeToRemediate.footer")}</p>
                  }
                  generatorName="raw"
                  generatorType="textBox"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.meanTimeToRemediate.title")}
                />
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Graphic
                  bsHeight={160}
                  documentName="severity"
                  documentType="gauge"
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.gauge.severity.footer")}</p>
                  }
                  generatorName="generic"
                  generatorType="c3"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.gauge.severity.title")}
                />
              </Col>
              <Col md={6}>
                <Graphic
                  bsHeight={160}
                  documentName="resources"
                  documentType="pieChart"
                  entity={entity}
                  footer={
                    <React.Fragment>
                      <p>{translate.t("analytics.pieChart.resources.footer.intro")}</p>
                      <ul>
                        <li>{translate.t("analytics.pieChart.resources.footer.environments")}</li>
                        <li>{translate.t("analytics.pieChart.resources.footer.repositories")}</li>
                      </ul>
                      <p>{translate.t("analytics.pieChart.resources.footer.final")}</p>
                    </React.Fragment>
                  }
                  generatorName="generic"
                  generatorType="c3"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.pieChart.resources.title")}
                />
              </Col>
            </Row>
            <Row>
          <Col md={12}>
            <Graphic
              bsHeight={320}
              documentName="whereToFindings"
              documentType="disjointForceDirectedGraph"
              entity={entity}
              footer={
                <ul>
                  <li>{translate.t("analytics.disjointForceDirectedGraph.whereToFindings.footer.grey")}</li>
                  <li>{translate.t("analytics.disjointForceDirectedGraph.whereToFindings.footer.redAndGreen")}</li>
                  <li>{translate.t("analytics.disjointForceDirectedGraph.whereToFindings.footer.size")}</li>
                </ul>
              }
              generatorName="whereToFindings"
              generatorType="disjointForceDirectedGraph"
              reportMode={reportMode}
              subject={subject}
              title={translate.t("analytics.disjointForceDirectedGraph.whereToFindings.title")}
            />
          </Col>
        </Row>
          </React.Fragment>
        ) : undefined}
      </Grid>
      {doesEntityMatch("group") ? (
        <React.Fragment>
          <hr />
          <Grid fluid={true}>
            <Row>
              <Col
                md={12}
                onMouseEnter={forcesPanelOnEnter}
                onMouseLeave={forcesPanelOnLeave}
              >
                <Panel expanded={isForcesDescriptionExpanded}>
                  <Panel.Heading>
                    <Panel.Title>
                      <h1 className={styles.centerTitle}>
                        {translate.t("analytics.sections.forces.title")}
                      </h1>
                    </Panel.Title>
                  </Panel.Heading>
                  <Panel.Collapse>
                    <Panel.Body>
                      <p>{translate.t("analytics.textBox.forcesStatus.footer.intro")}</p>
                      <ul>
                        <li>{translate.t("analytics.textBox.forcesStatus.footer.smart")}</li>
                        <li>{translate.t("analytics.textBox.forcesStatus.footer.breaks")}</li>
                        <li>{translate.t("analytics.textBox.forcesStatus.footer.stats")}</li>
                      </ul>
                    </Panel.Body>
                  </Panel.Collapse>
                </Panel>
              </Col>
            </Row>
            <div className={styles.separatorTitleFromCharts} />
            <Row>
              <Col md={3}>
                <Graphic
                  bsHeight={80}
                  documentName="forcesStatus"
                  documentType="textBox"
                  entity={entity}
                  generatorName="raw"
                  generatorType="textBox"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.forcesStatus.title")}
                />
              </Col>
              <Col md={3}>
                <Graphic
                  bsHeight={80}
                  documentName="forcesUsage"
                  documentType="textBox"
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.textBox.forcesUsage.footer")}</p>
                  }
                  generatorName="raw"
                  generatorType="textBox"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.forcesUsage.title")}
                />
              </Col>
              <Col md={3}>
                <Graphic
                  bsHeight={80}
                  documentName="forcesAutomatizedVulns"
                  documentType="textBox"
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.textBox.forcesAutomatizedVulns.footer")}</p>
                  }
                  generatorName="raw"
                  generatorType="textBox"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.forcesAutomatizedVulns.title")}
                />
              </Col>
              <Col md={3}>
                <Graphic
                  bsHeight={80}
                  documentName="forcesRepositoriesAndBranches"
                  documentType="textBox"
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.textBox.forcesRepositoriesAndBranches.footer")}</p>
                  }
                  generatorName="raw"
                  generatorType="textBox"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.forcesRepositoriesAndBranches.title")}
                />
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Graphic
                  bsHeight={160}
                  documentName="forcesSecurityCommitment"
                  documentType="gauge"
                  entity={entity}
                  footer={
                    <React.Fragment>
                      <p>{translate.t("analytics.gauge.forcesSecurityCommitment.footer.intro")}</p>
                      <ul>
                        <li>{translate.t("analytics.gauge.forcesSecurityCommitment.footer.strictMode")}</li>
                        <li>{translate.t("analytics.gauge.forcesSecurityCommitment.footer.acceptedRisk")}</li>
                      </ul>
                      <p>{translate.t("analytics.gauge.forcesSecurityCommitment.footer.conclusion")}</p>
                    </React.Fragment>
                  }
                  generatorName="generic"
                  generatorType="c3"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.gauge.forcesSecurityCommitment.title")}
                />
              </Col>
              <Col md={6}>
                <Graphic
                  bsHeight={160}
                  documentName="forcesBuildsRisk"
                  documentType="gauge"
                  entity={entity}
                  footer={
                    <React.Fragment>
                      <p>{translate.t("analytics.gauge.forcesBuildsRisk.footer.intro")}</p>
                      <ul>
                        <li>{translate.t("analytics.gauge.forcesBuildsRisk.footer.vulnerableBuilds")}</li>
                        <li>{translate.t("analytics.gauge.forcesBuildsRisk.footer.preventedVulnerableBuilds")}</li>
                      </ul>
                    </React.Fragment>
                  }
                  generatorName="generic"
                  generatorType="c3"
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.gauge.forcesBuildsRisk.title")}
                />
              </Col>
            </Row>
          </Grid>
        </React.Fragment>
      ) : undefined}
      {reportMode ? undefined : (
        <ChartsGenericViewExtras {...props} />
      )}
    </React.StrictMode>
  );
};

export { chartsGenericView as ChartsGenericView };
