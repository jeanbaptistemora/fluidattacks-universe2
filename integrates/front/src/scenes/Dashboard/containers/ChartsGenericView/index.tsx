/* eslint-disable react/forbid-component-props */
import React, { useCallback, useState } from "react";

import { Col100, Col33, Col50 } from "./components/ChartCols";

import { Graphic } from "graphics/components/Graphic";
import { ChartsGenericViewExtras } from "scenes/Dashboard/containers/ChartsGenericView/components/Extras";
import styles from "scenes/Dashboard/containers/ChartsGenericView/index.css";
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
import { translate } from "utils/translations/translate";

const ChartsGenericView: React.FC<IChartsGenericViewProps> = (
  props: IChartsGenericViewProps
): JSX.Element => {
  const { bgChange, entity, reportMode, subject } = props;

  const graphInfoLink = "https://docs.fluidattacks.com/machine/web/analytics/";

  const [isForcesDescriptionExpanded, setIsForcesDescriptionExpanded] =
    useState(reportMode);

  const forcesPanelOnEnter: () => void = useCallback((): void => {
    setIsForcesDescriptionExpanded(true);
  }, []);

  const forcesPanelOnLeave: () => void = useCallback((): void => {
    setIsForcesDescriptionExpanded(reportMode);
  }, [reportMode]);

  const doesEntityMatch: (entities: EntityType[]) => boolean = (
    entities: EntityType[]
  ): boolean => entities.includes(entity);

  const reportModeClassName: string = reportMode ? "report-mode" : "";
  const backgroundColorClassName: string = bgChange ? "report-bg-change" : "";
  const reportClassName: string =
    `${reportModeClassName} ${backgroundColorClassName}`.trim();

  return (
    <React.StrictMode>
      <div className={`center ${reportClassName}`.trim()}>
        {doesEntityMatch(["organization", "portfolio"]) ? (
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"cvssfBenchmarking"}
                documentType={"stackedBarChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"stackedBarChart"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t(
                  "analytics.stackedBarChart.cvssfBenchmarking.title"
                )}
              />
            </Col100>
          </RowCenter>
        ) : undefined}
        {doesEntityMatch(["group", "organization", "portfolio"]) ? (
          <React.Fragment>
            <RowCenter>
              <Col100>
                <Graphic
                  bsHeight={320}
                  className={"g1"}
                  documentName={"mttrBenchmarkingCvssf"}
                  documentType={"barChart"}
                  entity={entity}
                  generatorName={"generic"}
                  generatorType={"c3"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.barChart.mttrBenchmarking.title"
                  )}
                />
              </Col100>
            </RowCenter>
            <RowCenter>
              <Col100>
                <Graphic
                  bsHeight={320}
                  className={"g1"}
                  documentName={"exposedOverTimeCvssf"}
                  documentType={"stackedBarChart"}
                  entity={entity}
                  generatorName={"generic"}
                  generatorType={"c3"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.stackedBarChart.exposedOverTimeCvssf.title"
                  )}
                />
              </Col100>
            </RowCenter>
            <RowCenter>
              <Col100>
                <Graphic
                  bsHeight={320}
                  className={"g1"}
                  documentName={"topVulnerabilitiesCvssf"}
                  documentType={"barChart"}
                  entity={entity}
                  generatorName={"generic"}
                  generatorType={"c3"}
                  infoLink={`${graphInfoLink}common`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.barChart.topVulnerabilities.title"
                  )}
                />
              </Col100>
            </RowCenter>
          </React.Fragment>
        ) : undefined}
        {doesEntityMatch(["organization", "portfolio"]) ? (
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"exposedByGroups"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("analytics.barChart.exposureByGroups")}
              />
            </Col100>
          </RowCenter>
        ) : undefined}
        {doesEntityMatch(["group", "organization", "portfolio"]) ? (
          <React.Fragment>
            <RowCenter>
              <Col100>
                <Graphic
                  bsHeight={320}
                  className={"g1"}
                  documentName={"riskOverTimeCvssf"}
                  documentType={"stackedBarChart"}
                  entity={entity}
                  generatorName={"generic"}
                  generatorType={"c3"}
                  infoLink={`${graphInfoLink}common`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.stackedBarChart.riskOverTime.title"
                  )}
                />
              </Col100>
            </RowCenter>
            <RowCenter>
              <Col100>
                <Graphic
                  bsHeight={320}
                  className={"g1"}
                  documentName={"distributionOverTimeCvssf"}
                  documentType={"stackedBarChart"}
                  entity={entity}
                  generatorName={"generic"}
                  generatorType={"stackedBarChart"}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.stackedBarChart.distributionOverTimeCvssf.title"
                  )}
                />
              </Col100>
            </RowCenter>
            <RowCenter>
              <Col50>
                <Graphic
                  bsHeight={160}
                  className={"g2"}
                  documentName={"treatmentCvssf"}
                  documentType={"pieChart"}
                  entity={entity}
                  generatorName={"generic"}
                  generatorType={"c3"}
                  infoLink={`${graphInfoLink}common#vulnerabilities-treatment`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.pieChart.treatment.title")}
                />
              </Col50>
              <Col50>
                <Graphic
                  bsHeight={160}
                  className={"g2"}
                  documentName={"vulnerabilitiesBySourceCvssf"}
                  documentType={"pieChart"}
                  entity={entity}
                  generatorName={"generic"}
                  generatorType={"c3"}
                  infoLink={`${graphInfoLink}common#vulnerabilities-by-source`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("tagIndicator.vulnerabilitiesByType")}
                />
              </Col50>
            </RowCenter>
            <RowCenter>
              <Col50>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"totalFindings"}
                  documentType={"textBox"}
                  entity={entity}
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  infoLink={`${graphInfoLink}organization#total-types`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.totalTypes.title")}
                />
              </Col50>
              <Col50>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"vulnerabilitiesWithUndefinedTreatment"}
                  documentType={"textBox"}
                  entity={entity}
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  infoLink={`${graphInfoLink}groups#vulnerabilities-with-not-defined-treatment`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.textBox.vulnsWithUndefinedTreatment.title"
                  )}
                />
              </Col50>
            </RowCenter>
            <RowCenter>
              <Col33>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"findingsBeingReattacked"}
                  documentType={"textBox"}
                  entity={entity}
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  infoLink={`${graphInfoLink}common#vulnerabilities-being-re-attacked`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.textBox.findingsBeingReattacked.title"
                  )}
                />
              </Col33>
              <Col33>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"daysSinceLastRemediation"}
                  documentType={"textBox"}
                  entity={entity}
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  infoLink={`${graphInfoLink}common#days-since-last-remediation`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.textBox.daysSinceLastRemediation.title"
                  )}
                />
              </Col33>
              <Col33>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"totalVulnerabilities"}
                  documentType={"textBox"}
                  entity={entity}
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  infoLink={`${graphInfoLink}common#total-vulnerabilities`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.textBox.totalVulnerabilities.title"
                  )}
                />
              </Col33>
            </RowCenter>
            <RowCenter>
              <Col50>
                <Graphic
                  bsHeight={160}
                  className={"g2"}
                  documentName={"severity"}
                  documentType={"gauge"}
                  entity={entity}
                  generatorName={"generic"}
                  generatorType={"c3"}
                  infoLink={`${graphInfoLink}common#severity`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.gauge.severity.title")}
                />
              </Col50>
              <Col50>
                <Graphic
                  bsHeight={160}
                  className={"g2"}
                  documentName={"rootResources"}
                  documentType={"pieChart"}
                  entity={entity}
                  generatorName={"generic"}
                  generatorType={"c3"}
                  infoLink={`${graphInfoLink}common#active-resources-distribution`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.pieChart.resources.title")}
                />
              </Col50>
            </RowCenter>
          </React.Fragment>
        ) : undefined}
        {doesEntityMatch(["group"]) ? (
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"whereToFindings"}
                documentType={"disjointForceDirectedGraph"}
                entity={entity}
                generatorName={"whereToFindings"}
                generatorType={"disjointForceDirectedGraph"}
                infoLink={`${graphInfoLink}groups#systems-risk`}
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
      {doesEntityMatch(["group", "organization", "portfolio"]) ? (
        <div className={reportClassName}>
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
                infoLink={`${graphInfoLink}common#vulnerabilities-by-tag`}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tagIndicator.vulnerabilitiesByTag")}
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
                infoLink={`${graphInfoLink}common#vulnerabilities-by-level`}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tagIndicator.vulnerabilitiesByLevel")}
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
                infoLink={`${graphInfoLink}common#accepted-vulnerabilities-by-user`}
                reportMode={reportMode}
                subject={subject}
                title={translate.t(
                  "tagIndicator.acceptedVulnerabilitiesByUser"
                )}
              />
            </Col100>
          </RowCenter>
          {doesEntityMatch(["organization", "portfolio"]) ? (
            <React.Fragment>
              <RowCenter>
                <Col100>
                  <Graphic
                    bsHeight={320}
                    className={"g1"}
                    documentName={"remediatedGroup"}
                    documentType={"stackedBarChart"}
                    entity={entity}
                    generatorName={"generic"}
                    generatorType={"stackedBarChart"}
                    infoLink={`${graphInfoLink}portfolio#how-many-vulnerabilities-are-remediated-closed`}
                    reportMode={reportMode}
                    subject={subject}
                    title={translate.t("tagIndicator.remediatedVuln")}
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
                    generatorType={"stackedBarChart"}
                    infoLink={`${graphInfoLink}portfolio#how-many-vulnerabilities-are-remediated-and-accepted`}
                    reportMode={reportMode}
                    subject={subject}
                    title={translate.t("tagIndicator.remediatedAcceptedVuln")}
                  />
                </Col100>
              </RowCenter>
              <RowCenter>
                <Col100>
                  <Graphic
                    bsHeight={320}
                    className={"g1"}
                    documentName={"finding"}
                    documentType={"barChart"}
                    entity={entity}
                    generatorName={"generic"}
                    generatorType={"c3"}
                    infoLink={`${graphInfoLink}portfolio#findings-by-group`}
                    reportMode={reportMode}
                    subject={subject}
                    title={translate.t("tagIndicator.findingsGroup")}
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
                    infoLink={`${graphInfoLink}portfolio#open-findings-by-group`}
                    reportMode={reportMode}
                    subject={subject}
                    title={translate.t("tagIndicator.openFindingsGroup")}
                  />
                </Col100>
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
                    infoLink={`${graphInfoLink}portfolio#top-oldest-findings`}
                    reportMode={reportMode}
                    subject={subject}
                    title={translate.t("tagIndicator.topOldestFindings")}
                  />
                </Col100>
              </RowCenter>
              <RowCenter>
                <Col50>
                  <Graphic
                    bsHeight={160}
                    className={"g2"}
                    documentName={"vulnerabilitiesWithUndefinedTreatment"}
                    documentType={"pieChart"}
                    entity={entity}
                    generatorName={"generic"}
                    generatorType={"c3"}
                    infoLink={`${graphInfoLink}portfolio#treatmentless-by-group`}
                    reportMode={reportMode}
                    subject={subject}
                    title={translate.t("tagIndicator.undefinedTitle")}
                  />
                </Col50>
                <Col50>
                  <Graphic
                    bsHeight={160}
                    className={"g2"}
                    documentName={"vulnerabilitiesByTreatments"}
                    documentType={"pieChart"}
                    entity={entity}
                    generatorName={"generic"}
                    generatorType={"c3"}
                    infoLink={`${graphInfoLink}common#vulnerabilities-by-treatments`}
                    reportMode={reportMode}
                    subject={subject}
                    title={translate.t(
                      "tagIndicator.vulnerabilitiesByTreatments"
                    )}
                  />
                </Col50>
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
                    infoLink={`${graphInfoLink}portfolio#vulnerabilities-by-group`}
                    reportMode={reportMode}
                    subject={subject}
                    title={translate.t("tagIndicator.vulnsGroups")}
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
                    infoLink={`${graphInfoLink}portfolio#open-vulnerabilities-by-group`}
                    reportMode={reportMode}
                    subject={subject}
                    title={translate.t("tagIndicator.openVulnsGroups")}
                  />
                </Col50>
              </RowCenter>
            </React.Fragment>
          ) : undefined}
          {doesEntityMatch(["group"]) ? (
            <Row>
              <Col50>
                <Graphic
                  bsHeight={160}
                  className={"g2"}
                  documentName={"vulnerabilitiesByTreatments"}
                  documentType={"pieChart"}
                  entity={entity}
                  generatorName={"generic"}
                  generatorType={"c3"}
                  infoLink={`${graphInfoLink}common#vulnerabilities-by-number-of-changes-in-treatment`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "tagIndicator.vulnerabilitiesByTreatments"
                  )}
                />
              </Col50>
            </Row>
          ) : undefined}
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"acceptedVulnerabilitiesBySeverity"}
                documentType={"stackedBarChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"stackedBarChart"}
                infoLink={`${graphInfoLink}common#accepted-vulnerabilities-by-severity`}
                reportMode={reportMode}
                subject={subject}
                title={translate.t(
                  "tagIndicator.acceptedVulnerabilitiesBySeverity"
                )}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"meanTimeToRemediateCvssf"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                infoLink={`${graphInfoLink}common#mean-average-days-to-remediate`}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("tagIndicator.meanRemediate")}
              />
            </Col100>
          </RowCenter>
        </div>
      ) : undefined}
      {doesEntityMatch(["organization", "portfolio"]) ? (
        <div className={reportClassName}>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"groupsByTag"}
                documentType={"heatMapChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"heatMapChart"}
                infoLink={`${graphInfoLink}portfolio#tags-by-groups`}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("analytics.heatMapChart.groupsByTag")}
              />
            </Col100>
          </RowCenter>
        </div>
      ) : undefined}
      {doesEntityMatch(["group"]) ? (
        <div className={reportClassName}>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"findingsByTag"}
                documentType={"heatMapChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"heatMapChart"}
                infoLink={`${graphInfoLink}groups#findings-by-tags`}
                reportMode={reportMode}
                subject={subject}
                title={translate.t("analytics.heatMapChart.findingsByTag")}
              />
            </Col100>
          </RowCenter>
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
              <Col33>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"forcesStatus"}
                  documentType={"textBox"}
                  entity={entity}
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  infoLink={`${graphInfoLink}groups#service-status`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.forcesStatus.title")}
                />
              </Col33>
              <Col33>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"forcesUsage"}
                  documentType={"textBox"}
                  entity={entity}
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  infoLink={`${graphInfoLink}groups#service-usage`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.textBox.forcesUsage.title")}
                />
              </Col33>
              <Col33>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"forcesRepositoriesAndBranches"}
                  documentType={"textBox"}
                  entity={entity}
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  infoLink={`${graphInfoLink}groups#repositories-and-branches`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t(
                    "analytics.textBox.forcesRepositoriesAndBranches.title"
                  )}
                />
              </Col33>
            </RowCenter>
            <RowCenter>
              <Col50>
                <Graphic
                  bsHeight={160}
                  className={"g2"}
                  documentName={"forcesSecurityCommitment"}
                  documentType={"gauge"}
                  entity={entity}
                  generatorName={"generic"}
                  generatorType={"c3"}
                  infoLink={`${graphInfoLink}groups#your-commitment-towards-security`}
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
                  generatorName={"generic"}
                  generatorType={"c3"}
                  infoLink={`${graphInfoLink}groups#builds-risk`}
                  reportMode={reportMode}
                  subject={subject}
                  title={translate.t("analytics.gauge.forcesBuildsRisk.title")}
                />
              </Col50>
            </RowCenter>
          </div>
        </div>
      ) : undefined}
      {reportMode ? undefined : (
        <ChartsGenericViewExtras
          bgChange={bgChange}
          entity={entity}
          reportMode={reportMode}
          subject={subject}
        />
      )}
    </React.StrictMode>
  );
};

export { ChartsGenericView };
