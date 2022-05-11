/* eslint-disable react/forbid-component-props */
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

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
  RowCenter,
} from "styles/styledComponents";

const ChartsGenericView: React.FC<IChartsGenericViewProps> = ({
  bgChange,
  entity,
  reportMode,
  subject,
}: IChartsGenericViewProps): JSX.Element => {
  const { t } = useTranslation();
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
                infoLink={`${graphInfoLink}${entity}#remediation-rate-benchmarking`}
                reportMode={reportMode}
                subject={subject}
                title={t("analytics.stackedBarChart.cvssfBenchmarking.title")}
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
                  infoLink={`${graphInfoLink}common#mttr-benchmarking`}
                  reportMode={reportMode}
                  subject={subject}
                  title={t("analytics.barChart.mttrBenchmarking.title")}
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
                  infoLink={`${graphInfoLink}common#total-exposure`}
                  reportMode={reportMode}
                  subject={subject}
                  title={t(
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
                  generatorType={"barChart"}
                  infoLink={`${graphInfoLink}common`}
                  reportMode={reportMode}
                  subject={subject}
                  title={t("analytics.barChart.topVulnerabilities.title")}
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
                generatorType={"barChart"}
                infoLink={`${graphInfoLink}${entity}#open-severity-by-groups`}
                reportMode={reportMode}
                subject={subject}
                title={t("analytics.barChart.exposureByGroups")}
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
                  title={t("analytics.stackedBarChart.riskOverTime.title")}
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
                  infoLink={`${graphInfoLink}common#distribution-over-time`}
                  reportMode={reportMode}
                  subject={subject}
                  title={t(
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
                  title={t("analytics.pieChart.treatment.title")}
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
                  title={t("tagIndicator.vulnerabilitiesByType")}
                />
              </Col50>
            </RowCenter>
            <RowCenter>
              <Col33>
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
                  title={t("analytics.textBox.totalTypes.title")}
                />
              </Col33>
              <Col33>
                <Graphic
                  bsHeight={80}
                  className={"g3"}
                  documentName={"daysUntilZeroExposition"}
                  documentType={"textBox"}
                  entity={entity}
                  generatorName={"raw"}
                  generatorType={"textBox"}
                  infoLink={`${graphInfoLink}common#days-until-zero-exposure`}
                  reportMode={reportMode}
                  subject={subject}
                  title={t("analytics.textBox.daysUntilZeroExposition.title")}
                />
              </Col33>
              <Col33>
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
                  title={t(
                    "analytics.textBox.vulnsWithUndefinedTreatment.title"
                  )}
                />
              </Col33>
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
                  title={t("analytics.textBox.findingsBeingReattacked.title")}
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
                  title={t("analytics.textBox.daysSinceLastRemediation.title")}
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
                  title={t("analytics.textBox.totalVulnerabilities.title")}
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
                  title={t("analytics.gauge.severity.title")}
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
                  title={t("analytics.pieChart.resources.title")}
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
                title={t(
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
                title={t("tagIndicator.vulnerabilitiesByTag")}
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
                title={t("tagIndicator.vulnerabilitiesByLevel")}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"acceptedVulnerabilitiesByUser"}
                documentType={"stackedBarChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"stackedBarChart"}
                infoLink={`${graphInfoLink}common#accepted-vulnerabilities-by-user`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.acceptedVulnerabilitiesByUser")}
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
                documentName={"eventualities"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"barChart"}
                infoLink={`${graphInfoLink}portfolio#unsolved-events-by-groups`}
                reportMode={reportMode}
                subject={subject}
                title={t("analytics.barChart.eventualities")}
              />
            </Col100>
          </RowCenter>
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
                title={t("tagIndicator.remediatedVuln")}
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
                title={t("tagIndicator.remediatedAcceptedVuln")}
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
                generatorType={"barChart"}
                infoLink={`${graphInfoLink}${entity}#types-of-vulnerabilities-by-group`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.findingsGroup")}
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
                generatorType={"barChart"}
                infoLink={`${graphInfoLink}${entity}#open-types-of-vulnerabilities-by-group`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.openFindingsGroup")}
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
                generatorType={"barChart"}
                infoLink={`${graphInfoLink}${entity}#top-oldest-types-of-vulnerabilities`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.topOldestFindings")}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col50>
              <Graphic
                bsHeight={160}
                className={"g2"}
                documentName={"assignedVulnerabilities"}
                documentType={"pieChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.assignedVulnerabilities")}
              />
            </Col50>
            <Col50>
              <Graphic
                bsHeight={160}
                className={"g2"}
                documentName={"vulnerabilitiesWithUndefinedTreatment"}
                documentType={"pieChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                infoLink={`${graphInfoLink}${entity}#undefined-treatment-by-group`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.undefinedTitle")}
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
                infoLink={`${graphInfoLink}${entity}#vulnerabilities-by-group`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.vulnsGroups")}
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
                infoLink={`${graphInfoLink}${entity}#open-vulnerabilities-by-group`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.openVulnsGroups")}
              />
            </Col50>
          </RowCenter>
        </div>
      ) : undefined}
      {doesEntityMatch(["group"]) ? (
        <div className={reportClassName}>
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
                infoLink={`${graphInfoLink}common#vulnerabilities-by-number-of-treatment-changes`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.vulnerabilitiesByTreatments")}
              />
            </Col50>
            <Col50>
              <Graphic
                bsHeight={160}
                className={"g2"}
                documentName={"assignedVulnerabilities"}
                documentType={"pieChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.assignedVulnerabilities")}
              />
            </Col50>
          </RowCenter>
        </div>
      ) : undefined}
      {doesEntityMatch(["group", "organization", "portfolio"]) ? (
        <div className={reportClassName}>
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
                title={t("tagIndicator.acceptedVulnerabilitiesBySeverity")}
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
                generatorType={"barChart"}
                infoLink={`${graphInfoLink}common#mean-average-days-to-remediate`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.meanRemediate")}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"assignedVulnerabilitiesCvssf"}
                documentType={"stackedBarChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"stackedBarChart"}
                reportMode={reportMode}
                subject={subject}
                title={t(
                  "analytics.stackedBarChart.assignedVulnerabilities.title"
                )}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"touchedFiles"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"barChart"}
                reportMode={reportMode}
                subject={subject}
                title={t("analytics.barChart.touchedFiles.title")}
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
                title={t("analytics.heatMapChart.groupsByTag")}
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
                title={t("analytics.heatMapChart.findingsByTag")}
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
                    <h1>{t("analytics.sections.forces.title")}</h1>
                  </PanelCollapseHeader>
                  <PanelCollapseBody>
                    <p>{t("analytics.textBox.forcesStatus.footer.intro")}</p>
                    <ul>
                      <li>
                        {t("analytics.textBox.forcesStatus.footer.smart")}
                      </li>
                      <li>
                        {t("analytics.textBox.forcesStatus.footer.breaks")}
                      </li>
                      <li>
                        {t("analytics.textBox.forcesStatus.footer.stats")}
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
                  title={t("analytics.textBox.forcesStatus.title")}
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
                  title={t("analytics.textBox.forcesUsage.title")}
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
                  title={t(
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
                  title={t("analytics.gauge.forcesSecurityCommitment.title")}
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
                  title={t("analytics.gauge.forcesBuildsRisk.title")}
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
