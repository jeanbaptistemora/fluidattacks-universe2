/* eslint-disable react/forbid-component-props, fp/no-rest-parameters, react/jsx-props-no-spreading */
import { ChartsGenericViewExtras } from "scenes/Dashboard/containers/ChartsGenericView/components/Extras";
import { Graphic } from "graphics/components/Graphic";
import React from "react";
import styles from "scenes/Dashboard/containers/ChartsGenericView/index.css";
import { translate } from "utils/translations/translate";
import { Col100, Col25, Col33, Col50 } from "./components/ChartCols";
import type {
  EntityType,
  IChartsGenericViewProps,
} from "scenes/Dashboard/containers/ChartsGenericView/types";
import {
  PanelCollapse,
  PanelCollapseBody,
  PanelCollapseHeader,
  Row,
  RowCenter,
} from "styles/styledComponents";

const ChartsGenericView: React.FC<IChartsGenericViewProps> = (
  props: IChartsGenericViewProps
): JSX.Element => {
  const { entity, reportMode, subject } = props;

  const [
    isForcesDescriptionExpanded,
    setIsForcesDescriptionExpanded,
  ] = React.useState(reportMode);

  const forcesPanelOnEnter: () => void = React.useCallback((): void => {
    setIsForcesDescriptionExpanded(true);
  }, []);

  const forcesPanelOnLeave: () => void = React.useCallback((): void => {
    setIsForcesDescriptionExpanded(reportMode);
  }, [reportMode]);

  const doesEntityMatch: (...entities: EntityType[]) => boolean = (
    ...entities: EntityType[]
  ): boolean => entities.includes(entity);

  return (
    <React.StrictMode>
      <div className={"center"}>
        {doesEntityMatch("group", "organization", "portfolio") ? (
          <React.Fragment>
            <RowCenter>
              <Col100>
                <Graphic
                  bsHeight={320}
                  className={"g1"}
                  documentName={"riskOverTime"}
                  documentType={"stackedBarChart"}
                  entity={entity}
                  footer={
                    <React.Fragment>
                      <p>
                        {translate.t(
                          "analytics.stackedBarChart.riskOverTime.footer.intro"
                        )}
                      </p>
                      <ul>
                        <li>
                          {translate.t(
                            "analytics.stackedBarChart.riskOverTime.footer.opened"
                          )}
                        </li>
                        <li>
                          {translate.t(
                            "analytics.stackedBarChart.riskOverTime.footer.accepted"
                          )}
                        </li>
                        <li>
                          {translate.t(
                            "analytics.stackedBarChart.riskOverTime.footer.closed"
                          )}
                        </li>
                      </ul>
                    </React.Fragment>
                  }
                  generatorName={"generic"}
                  generatorType={"c3"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.stackedBarChart.riskOverTime.title"
                  )}
                />
              </Col100>
            </RowCenter>
            <RowCenter>
              <Col50>
                <Graphic
                  bsHeight={160}
                  className={"g2"}
                  documentName={"status"}
                  documentType={"pieChart"}
                  entity={entity}
                  footer={
                    <p>
                      {translate.t("analytics.pieChart.status.footer.intro")}
                    </p>
                  }
                  generatorName={"generic"}
                  generatorType={"c3"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.pieChart.status.title")}
                />
              </Col50>
              <Col50>
                <Graphic
                  bsHeight={160}
                  className={"g2"}
                  documentName={"treatment"}
                  documentType={"pieChart"}
                  entity={entity}
                  footer={
                    <React.Fragment>
                      <p>
                        {translate.t(
                          "analytics.pieChart.treatment.footer.intro"
                        )}
                      </p>
                      <ul>
                        <li>
                          {translate.t(
                            "analytics.pieChart.treatment.footer.notDefined"
                          )}
                        </li>
                        <li>
                          {translate.t(
                            "analytics.pieChart.treatment.footer.inProgress"
                          )}
                        </li>
                        <li>
                          {translate.t(
                            "analytics.pieChart.treatment.footer.accepted"
                          )}
                        </li>
                        <li>
                          {translate.t(
                            "analytics.pieChart.treatment.footer.eternally"
                          )}
                        </li>
                      </ul>
                    </React.Fragment>
                  }
                  generatorName={"generic"}
                  generatorType={"c3"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.pieChart.treatment.title")}
                />
              </Col50>
            </RowCenter>
          </React.Fragment>
        ) : undefined}
        {doesEntityMatch("group", "organization") ? (
          <RowCenter>
            <Col33>
              <Graphic
                bsHeight={80}
                className={"g3"}
                documentName={"totalFindings"}
                documentType={"textBox"}
                entity={entity}
                footer={
                  <p>{translate.t("analytics.textBox.totalFindings.footer")}</p>
                }
                generatorName={"raw"}
                generatorType={"textBox"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("analytics.textBox.totalFindings.title")}
              />
            </Col33>
            <Col33>
              <Graphic
                bsHeight={80}
                className={"g3"}
                documentName={"totalVulnerabilities"}
                documentType={"textBox"}
                entity={entity}
                footer={
                  <p>
                    {translate.t(
                      "analytics.textBox.totalVulnerabilities.footer"
                    )}
                  </p>
                }
                generatorName={"raw"}
                generatorType={"textBox"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t(
                  "analytics.textBox.totalVulnerabilities.title"
                )}
              />
            </Col33>
            <Col33>
              <Graphic
                bsHeight={80}
                className={"g3"}
                documentName={"vulnsWithUndefinedTreatment"}
                documentType={"textBox"}
                entity={entity}
                footer={
                  <p>
                    {translate.t(
                      "analytics.textBox.vulnsWithUndefinedTreatment.footer"
                    )}
                  </p>
                }
                generatorName={"raw"}
                generatorType={"textBox"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t(
                  "analytics.textBox.vulnsWithUndefinedTreatment.title"
                )}
              />
            </Col33>
          </RowCenter>
        ) : undefined}
        {doesEntityMatch("group", "organization", "portfolio") ? (
          <React.Fragment>
            <RowCenter>
              <Col50>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"findingsBeingReattacked"}
                  documentType={"textBox"}
                  entity={entity}
                  footer={
                    <p>
                      {translate.t(
                        "analytics.textBox.findingsBeingReattacked.footer"
                      )}
                    </p>
                  }
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.textBox.findingsBeingReattacked.title"
                  )}
                />
              </Col50>
              <Col50>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"daysSinceLastRemediation"}
                  documentType={"textBox"}
                  entity={entity}
                  footer={
                    <p>
                      {translate.t(
                        "analytics.textBox.daysSinceLastRemediation.footer"
                      )}
                    </p>
                  }
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.textBox.daysSinceLastRemediation.title"
                  )}
                />
              </Col50>
            </RowCenter>
            <RowCenter>
              <Col50>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"meanTimeToRemediate"}
                  documentType={"textBox"}
                  entity={entity}
                  footer={
                    <p>
                      {translate.t(
                        "analytics.textBox.meanTimeToRemediate.footer"
                      )}
                    </p>
                  }
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.textBox.meanTimeToRemediate.title"
                  )}
                />
              </Col50>
              <Col50>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"meanTimeToRemediateNonTreated"}
                  documentType={"textBox"}
                  entity={entity}
                  footer={
                    <p>
                      {translate.t(
                        "analytics.textBox.meanTimeToRemediateNonTreated.footer"
                      )}
                    </p>
                  }
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.textBox.meanTimeToRemediateNonTreated.title"
                  )}
                />
              </Col50>
            </RowCenter>
            <RowCenter>
              <Col50>
                <Graphic
                  bsHeight={160}
                  className={"g2"}
                  documentName={"severity"}
                  documentType={"gauge"}
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.gauge.severity.footer")}</p>
                  }
                  generatorName={"generic"}
                  generatorType={"c3"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.gauge.severity.title")}
                />
              </Col50>
              <Col50>
                <Graphic
                  bsHeight={160}
                  className={"g2"}
                  documentName={"resources"}
                  documentType={"pieChart"}
                  entity={entity}
                  footer={
                    <React.Fragment>
                      <p>
                        {translate.t(
                          "analytics.pieChart.resources.footer.intro"
                        )}
                      </p>
                      <ul>
                        <li>
                          {translate.t(
                            "analytics.pieChart.resources.footer.environments"
                          )}
                        </li>
                        <li>
                          {translate.t(
                            "analytics.pieChart.resources.footer.repositories"
                          )}
                        </li>
                      </ul>
                      <p>
                        {translate.t(
                          "analytics.pieChart.resources.footer.final"
                        )}
                      </p>
                    </React.Fragment>
                  }
                  generatorName={"generic"}
                  generatorType={"c3"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.pieChart.resources.title")}
                />
              </Col50>
            </RowCenter>
          </React.Fragment>
        ) : undefined}
        {doesEntityMatch("group") ? (
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"whereToFindings"}
                documentType={"disjointForceDirectedGraph"}
                entity={entity}
                footer={
                  <ul>
                    <li>
                      {translate.t(
                        "analytics.disjointForceDirectedGraph.whereToFindings.footer.grey"
                      )}
                    </li>
                    <li>
                      {translate.t(
                        "analytics.disjointForceDirectedGraph.whereToFindings.footer.redAndGreen"
                      )}
                    </li>
                    <li>
                      {translate.t(
                        "analytics.disjointForceDirectedGraph.whereToFindings.footer.size"
                      )}
                    </li>
                  </ul>
                }
                generatorName={"whereToFindings"}
                generatorType={"disjointForceDirectedGraph"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t(
                  "analytics.disjointForceDirectedGraph.whereToFindings.title"
                )}
              />
            </Col100>
          </RowCenter>
        ) : undefined}
      </div>
      {doesEntityMatch("portfolio") ? (
        <div className={"center"}>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"remediatedGroup"}
                documentType={"stackedBarChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.remediated_vuln")}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"remediatedAcceptedGroup"}
                documentType={"stackedBarChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.remediated_accepted_vuln")}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"findings"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.findings_group")}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"openFindings"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.open_findings_group")}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col50>
              <Graphic
                bsHeight={160}
                className={"g2"}
                documentName={"totalVulnerabilitiesStatus"}
                documentType={"pieChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.vulns_groups")}
              />
            </Col50>
            <Col50>
              <Graphic
                bsHeight={160}
                className={"g2"}
                documentName={"openVulnerabilitiesStatus"}
                documentType={"pieChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.open_vulns_groups")}
              />
            </Col50>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"topOldestFindings"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.topOldestFindings")}
              />
            </Col100>
          </RowCenter>
          <Row>
            <Col50>
              <Graphic
                bsHeight={160}
                className={"g2"}
                documentName={"vulnsWithUndefinedTreatment"}
                documentType={"pieChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.undefined_title")}
              />
            </Col50>
            <Col50>
              <Graphic
                bsHeight={80}
                className={"g3"}
                documentName={"totalVulnerabilities"}
                documentType={"textBox"}
                entity={entity}
                footer={
                  <p>
                    {translate.t(
                      "analytics.textBox.totalVulnerabilities.footer"
                    )}
                  </p>
                }
                generatorName={"raw"}
                generatorType={"textBox"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t(
                  "analytics.textBox.totalVulnerabilities.title"
                )}
              />
            </Col50>
          </Row>
        </div>
      ) : undefined}
      {doesEntityMatch("group", "organization", "portfolio") ? (
        <React.Fragment>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"vulnerabilitiesByTag"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.vulnerabilitiesByTag")}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"vulnerabilitiesByLevel"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.vulnerabilitiesByLevel")}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"acceptedVulnerabilitiesByUser"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t(
                  "tag_indicator.acceptedVulnerabilitiesByUser"
                )}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col50>
              <Graphic
                bsHeight={160}
                className={"g2"}
                documentName={"vulnerabilitiesByTreatments"}
                documentType={"pieChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.vulnerabilitiesByTreatments")}
              />
            </Col50>
            <Col50>
              <Graphic
                bsHeight={160}
                className={"g2"}
                documentName={"vulnerabilitiesByType"}
                documentType={"pieChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.vulnerabilitiesByType")}
              />
            </Col50>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"topFindingsByVulnerabilities"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t(
                  "tag_indicator.topFindingsByVulnerabilities"
                )}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"acceptedVulnsBySeverity"}
                documentType={"stackedBarChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t(
                  "tag_indicator.acceptedVulnerabilitiesBySeverity"
                )}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={160}
                className={"g2"}
                documentName={"meanTimeToRemediate"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tag_indicator.mean_remediate")}
              />
            </Col100>
          </RowCenter>
        </React.Fragment>
      ) : undefined}
      {doesEntityMatch("group") ? (
        <React.Fragment>
          <hr />
          <div className={"center"}>
            <RowCenter>
              <Col100
                onMouseEnter={forcesPanelOnEnter}
                onMouseLeave={forcesPanelOnLeave}
              >
                <PanelCollapse aria-expanded={isForcesDescriptionExpanded}>
                  <PanelCollapseHeader>
                    <h1>{translate.t("analytics.sections.forces.title")}</h1>
                  </PanelCollapseHeader>
                  <PanelCollapseBody>
                    <p>
                      {translate.t(
                        "analytics.textBox.forcesStatus.footer.intro"
                      )}
                    </p>
                    <ul>
                      <li>
                        {translate.t(
                          "analytics.textBox.forcesStatus.footer.smart"
                        )}
                      </li>
                      <li>
                        {translate.t(
                          "analytics.textBox.forcesStatus.footer.breaks"
                        )}
                      </li>
                      <li>
                        {translate.t(
                          "analytics.textBox.forcesStatus.footer.stats"
                        )}
                      </li>
                    </ul>
                  </PanelCollapseBody>
                </PanelCollapse>
              </Col100>
            </RowCenter>
            <div className={styles.separatorTitleFromCharts} />
            <RowCenter>
              <Col25>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"forcesStatus"}
                  documentType={"textBox"}
                  entity={entity}
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.forcesStatus.title")}
                />
              </Col25>
              <Col25>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"forcesUsage"}
                  documentType={"textBox"}
                  entity={entity}
                  footer={
                    <p>{translate.t("analytics.textBox.forcesUsage.footer")}</p>
                  }
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.forcesUsage.title")}
                />
              </Col25>
              <Col25>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"forcesAutomatizedVulns"}
                  documentType={"textBox"}
                  entity={entity}
                  footer={
                    <p>
                      {translate.t(
                        "analytics.textBox.forcesAutomatizedVulns.footer"
                      )}
                    </p>
                  }
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.textBox.forcesAutomatizedVulns.title"
                  )}
                />
              </Col25>
              <Col25>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"forcesRepositoriesAndBranches"}
                  documentType={"textBox"}
                  entity={entity}
                  footer={
                    <p>
                      {translate.t(
                        "analytics.textBox.forcesRepositoriesAndBranches.footer"
                      )}
                    </p>
                  }
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.textBox.forcesRepositoriesAndBranches.title"
                  )}
                />
              </Col25>
            </RowCenter>
            <RowCenter>
              <Col50>
                <Graphic
                  bsHeight={160}
                  className={"g2"}
                  documentName={"forcesSecurityCommitment"}
                  documentType={"gauge"}
                  entity={entity}
                  footer={
                    <React.Fragment>
                      <p>
                        {translate.t(
                          "analytics.gauge.forcesSecurityCommitment.footer.intro"
                        )}
                      </p>
                      <ul>
                        <li>
                          {translate.t(
                            "analytics.gauge.forcesSecurityCommitment.footer.strictMode"
                          )}
                        </li>
                        <li>
                          {translate.t(
                            "analytics.gauge.forcesSecurityCommitment.footer.acceptedRisk"
                          )}
                        </li>
                      </ul>
                      <p>
                        {translate.t(
                          "analytics.gauge.forcesSecurityCommitment.footer.conclusion"
                        )}
                      </p>
                    </React.Fragment>
                  }
                  generatorName={"generic"}
                  generatorType={"c3"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.gauge.forcesSecurityCommitment.title"
                  )}
                />
              </Col50>
              <Col50>
                <Graphic
                  bsHeight={160}
                  className={"g2"}
                  documentName={"forcesBuildsRisk"}
                  documentType={"gauge"}
                  entity={entity}
                  footer={
                    <React.Fragment>
                      <p>
                        {translate.t(
                          "analytics.gauge.forcesBuildsRisk.footer.intro"
                        )}
                      </p>
                      <ul>
                        <li>
                          {translate.t(
                            "analytics.gauge.forcesBuildsRisk.footer.vulnerableBuilds"
                          )}
                        </li>
                        <li>
                          {translate.t(
                            "analytics.gauge.forcesBuildsRisk.footer.preventedVulnerableBuilds"
                          )}
                        </li>
                      </ul>
                    </React.Fragment>
                  }
                  generatorName={"generic"}
                  generatorType={"c3"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.gauge.forcesBuildsRisk.title")}
                />
              </Col50>
            </RowCenter>
          </div>
        </React.Fragment>
      ) : undefined}
      {reportMode ? undefined : <ChartsGenericViewExtras {...props} />}
    </React.StrictMode>
  );
};

export { ChartsGenericView };
