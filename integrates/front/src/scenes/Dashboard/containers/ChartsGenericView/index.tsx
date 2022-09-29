/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable react/forbid-component-props */
import React, { useMemo } from "react";
import { useTranslation } from "react-i18next";

import { Col100, Col25, Col33, Col50 } from "./components/ChartCols";

import { Graphic } from "graphics/components/Graphic";
import { ChartsGenericViewExtras } from "scenes/Dashboard/containers/ChartsGenericView/components/Extras";
import styles from "scenes/Dashboard/containers/ChartsGenericView/index.css";
import type {
  EntityType,
  IChartsGenericViewProps,
} from "scenes/Dashboard/containers/ChartsGenericView/types";
import { PanelCollapseHeader, Row, RowCenter } from "styles/styledComponents";

export const ChartsView: React.FC<IChartsGenericViewProps> = ({
  bgChange,
  entity,
  reportMode,
  subject,
}: IChartsGenericViewProps): JSX.Element => {
  const { t } = useTranslation();
  const graphInfoLink = "https://docs.fluidattacks.com/machine/web/analytics/";

  const doesEntityMatch: (entities: EntityType[]) => boolean = (
    entities: EntityType[]
  ): boolean => entities.includes(entity);

  const reportModeClassName: string = useMemo((): string => {
    return reportMode ? "report-mode" : "";
  }, [reportMode]);
  const backgroundColorClassName: string = useMemo((): string => {
    return bgChange ? "report-bg-change" : "";
  }, [bgChange]);
  const reportClassName: string = useMemo((): string => {
    return `${reportModeClassName} ${backgroundColorClassName}`.trim();
  }, [reportModeClassName, backgroundColorClassName]);

  return (
    <React.StrictMode>
      {reportMode ? undefined : (
        <div className={"center ph3 mb3"}>
          <ChartsGenericViewExtras
            bgChange={bgChange}
            entity={entity}
            reportMode={reportMode}
            subject={subject}
          />
        </div>
      )}
      <div className={reportClassName}>
        <RowCenter>
          <Col100>
            <Graphic
              bsHeight={320}
              className={"g1"}
              documentName={"exposedOverTimeCvssf"}
              documentType={"stackedBarChart"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"stackedBarChart"}
              infoLink={`${graphInfoLink}common#exposure-over-time`}
              reportMode={reportMode}
              subject={subject}
              title={t("analytics.stackedBarChart.exposedOverTimeCvssf.title")}
            />
          </Col100>
        </RowCenter>
        <Col100>
          <div className={"flex flex-wrap justify-between"}>
            <div className={"pr3 w-33 relative"}>
              <Graphic
                bsHeight={80}
                className={"g3"}
                documentName={"remediationRateCvssf"}
                documentType={"textBox"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"textBox"}
                reportMode={reportMode}
                subject={subject}
                title={t("analytics.textBox.remediationRate.title")}
              />
            </div>
            <Col33>
              <Graphic
                bsHeight={80}
                className={"g3"}
                documentName={"openVulnerabilities"}
                documentType={"textBox"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"textBox"}
                reportMode={reportMode}
                subject={subject}
                title={t("analytics.textBox.openVulnerabilities.title")}
              />
            </Col33>
            <div className={"pl3 w-33 relative"}>
              <Graphic
                bsHeight={80}
                className={"g3"}
                documentName={"vulnerabilitiesWithUndefinedTreatment"}
                documentType={"textBox"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"textBox"}
                infoLink={`${graphInfoLink}common#vulnerabilities-with-no-treatment`}
                reportMode={reportMode}
                subject={subject}
                title={t("analytics.textBox.vulnsWithUndefinedTreatment.title")}
              />
            </div>
          </div>
        </Col100>
        <RowCenter>
          <Col100>
            <Graphic
              bsHeight={320}
              className={"g1"}
              documentName={"riskOverTimeCvssf"}
              documentType={"stackedBarChart"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"stackedBarChart"}
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
              infoLink={`${graphInfoLink}common`}
              reportMode={reportMode}
              subject={subject}
              title={t(
                "analytics.stackedBarChart.distributionOverTimeCvssf.title"
              )}
            />
          </Col100>
        </RowCenter>
        <RowCenter>
          <Col100>
            <Graphic
              bsHeight={320}
              className={"g1"}
              documentName={"exposureBenchmarkingCvssf"}
              documentType={"barChart"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"barChart"}
              infoLink={`${graphInfoLink}common#aggregated-exposure-benchmark`}
              reportMode={reportMode}
              subject={subject}
              title={t("analytics.barChart.exposureBenchmarkingCvssf")}
            />
          </Col100>
        </RowCenter>
        <RowCenter>
          <Col100>
            <Graphic
              bsHeight={320}
              className={"g1"}
              documentName={"exposureTrendsByCategories"}
              documentType={"barChart"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"barChart"}
              infoLink={`${graphInfoLink}common#exposure-trends-by-categories`}
              reportMode={reportMode}
              shouldDisplayAll={false}
              subject={subject}
              title={t("analytics.barChart.exposureTrendsByCategories")}
            />
          </Col100>
        </RowCenter>
        <RowCenter>
          <Col25>
            <Graphic
              bsHeight={80}
              className={"g3"}
              documentName={"daysSinceLastRemediation"}
              documentType={"textBox"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"textBox"}
              infoLink={`${graphInfoLink}common#days-since-last-remediation`}
              reportMode={reportMode}
              subject={subject}
              title={t("analytics.textBox.daysSinceLastRemediation.title")}
            />
          </Col25>
          <Col25>
            <Graphic
              bsHeight={80}
              className={"g3"}
              documentName={"meanTimeToReattack"}
              documentType={"textBox"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"textBox"}
              infoLink={`${graphInfoLink}common#mean-time-to-reattack`}
              reportMode={reportMode}
              subject={subject}
              title={t("analytics.textBox.meanTimeToReattack.title")}
            />
          </Col25>
          <Col25>
            <Graphic
              bsHeight={80}
              className={"g3"}
              documentName={"findingsBeingReattacked"}
              documentType={"textBox"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"textBox"}
              infoLink={`${graphInfoLink}common#vulnerabilities-being-re-attacked`}
              reportMode={reportMode}
              subject={subject}
              title={t("analytics.textBox.findingsBeingReattacked.title")}
            />
          </Col25>
          <Col25>
            <Graphic
              bsHeight={80}
              className={"g3"}
              documentName={"daysUntilZeroExposition"}
              documentType={"textBox"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"textBox"}
              infoLink={`${graphInfoLink}common#days-until-zero-exposure`}
              reportMode={reportMode}
              subject={subject}
              title={t("analytics.textBox.daysUntilZeroExposition.title")}
            />
          </Col25>
        </RowCenter>
      </div>
      {doesEntityMatch(["organization", "portfolio"]) ? (
        <div className={reportClassName}>
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
                infoLink={`${graphInfoLink}${entity}#exposure-remediation-rate-benchmark`}
                reportMode={reportMode}
                subject={subject}
                title={t("analytics.stackedBarChart.cvssfBenchmarking.title")}
              />
            </Col100>
          </RowCenter>
        </div>
      ) : undefined}
      <div className={reportClassName}>
        <RowCenter>
          <Col100>
            <Graphic
              bsHeight={320}
              className={"g1"}
              documentName={"mttrBenchmarkingCvssf"}
              documentType={"barChart"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"barChart"}
              infoLink={`${graphInfoLink}common`}
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
              documentName={"meanTimeToRemediateCvssf"}
              documentType={"barChart"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"barChart"}
              infoLink={`${graphInfoLink}common`}
              reportMode={reportMode}
              subject={subject}
              title={t("tagIndicator.meanRemediate")}
            />
          </Col100>
        </RowCenter>
      </div>
      {doesEntityMatch(["organization", "portfolio"]) ? (
        <div className={reportClassName}>
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
                infoLink={`${graphInfoLink}${entity}#how-many-vulnerabilities-are-remediated-and-accepted`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.remediatedAcceptedVuln")}
              />
            </Col100>
          </RowCenter>
        </div>
      ) : undefined}
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
              documentName={"assignedVulnerabilities"}
              documentType={"pieChart"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"c3"}
              infoLink={`${graphInfoLink}common#vulnerabilities-by-assignment`}
              reportMode={reportMode}
              subject={subject}
              title={t("tagIndicator.assignedVulnerabilities")}
            />
          </Col50>
        </RowCenter>
      </div>
      {doesEntityMatch(["organization", "portfolio"]) ? (
        <div className={reportClassName}>
          <RowCenter>
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
        </div>
      ) : undefined}
      <div className={reportClassName}>
        <Row>
          <Col50>
            <Graphic
              bsHeight={160}
              className={"g2"}
              documentName={"assignedVulnerabilitiesStatus"}
              documentType={"pieChart"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"c3"}
              infoLink={`${graphInfoLink}common#status-of-assigned-vulnerabilities`}
              reportMode={reportMode}
              subject={subject}
              title={t("tagIndicator.assignedVulnerabilitiesStatus")}
            />
          </Col50>
        </Row>
        <RowCenter>
          <Col33>
            <Graphic
              bsHeight={80}
              className={"g3"}
              documentName={"vulnerabilitiesRemediationCreated"}
              documentType={"textBox"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"textBox"}
              infoLink={`${graphInfoLink}common#sprint-exposure-increment`}
              reportMode={reportMode}
              subject={subject}
              title={t("analytics.textBox.remediationCreated.title")}
            />
          </Col33>
          <Col33>
            <Graphic
              bsHeight={80}
              className={"g3"}
              documentName={"vulnerabilitiesRemediationSolved"}
              documentType={"textBox"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"textBox"}
              infoLink={`${graphInfoLink}common#sprint-exposure-decrement`}
              reportMode={reportMode}
              subject={subject}
              title={t("analytics.textBox.remediationSolved.title")}
            />
          </Col33>
          <Col33>
            <Graphic
              bsHeight={80}
              className={"g3"}
              documentName={"vulnerabilitiesRemediationRemediated"}
              documentType={"textBox"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"textBox"}
              infoLink={`${graphInfoLink}common#sprint-exposure-change-overall`}
              reportMode={reportMode}
              subject={subject}
              title={t("analytics.textBox.remediationRemediated.title")}
            />
          </Col33>
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
      </div>
      {doesEntityMatch(["organization", "portfolio"]) ? (
        <div className={reportClassName}>
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
                infoLink={`${graphInfoLink}${entity}#open-exposure-by-groups`}
                reportMode={reportMode}
                subject={subject}
                title={t("analytics.barChart.exposureByGroups")}
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
        </div>
      ) : undefined}
      <div className={reportClassName}>
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
        <Row>
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
        </Row>
        <Row>
          <Col33>
            <Graphic
              bsHeight={80}
              className={"g3"}
              documentName={"totalFindings"}
              documentType={"textBox"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"textBox"}
              infoLink={`${graphInfoLink}common#total-types`}
              reportMode={reportMode}
              subject={subject}
              title={t("analytics.textBox.totalTypes.title")}
            />
          </Col33>
          <Col33>
            <Graphic
              bsHeight={80}
              className={"g3"}
              documentName={"totalVulnerabilities"}
              documentType={"textBox"}
              entity={entity}
              generatorName={"generic"}
              generatorType={"textBox"}
              infoLink={`${graphInfoLink}common#total-vulnerabilities`}
              reportMode={reportMode}
              subject={subject}
              title={t("analytics.textBox.totalVulnerabilities.title")}
            />
          </Col33>
        </Row>
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
                infoLink={`${graphInfoLink}${entity}#unsolved-events-by-groups`}
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
                documentName={"reportTechnique"}
                documentType={"pieChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                infoLink={`${graphInfoLink}common#report-technique`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.reportTechnique")}
              />
            </Col50>
          </RowCenter>
        </div>
      ) : undefined}
      {doesEntityMatch(["group"]) ? (
        <div className={reportClassName}>
          <RowCenter />
          <RowCenter>
            <Col50>
              <Graphic
                bsHeight={160}
                className={"g2"}
                documentName={"reportTechnique"}
                documentType={"pieChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                infoLink={`${graphInfoLink}common#report-technique`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.reportTechnique")}
              />
            </Col50>
            <Col50>
              <Graphic
                bsHeight={160}
                className={"g2"}
                documentName={"availability"}
                documentType={"pieChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                infoLink={`${graphInfoLink}groups#group-availability`}
                reportMode={reportMode}
                subject={subject}
                title={t("analytics.pieChart.availability.title")}
              />
            </Col50>
          </RowCenter>
        </div>
      ) : undefined}
      <div className={reportClassName}>
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
              infoLink={`${graphInfoLink}common`}
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
              infoLink={`${graphInfoLink}common#files-with-open-vulnerabilities-in-the-last-20-weeks`}
              reportMode={reportMode}
              subject={subject}
              title={t("analytics.barChart.touchedFiles.title")}
            />
          </Col100>
        </RowCenter>
      </div>
      {doesEntityMatch(["organization", "portfolio"]) ? (
        <div className={reportClassName}>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"availability"}
                documentType={"stackedBarChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"stackedBarChart"}
                infoLink={`${graphInfoLink}${entity}#groups-availability`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.groupsAvailability")}
              />
            </Col100>
          </RowCenter>
          <RowCenter>
            <Col100>
              <Graphic
                bsHeight={320}
                className={"g1"}
                documentName={"oldestEvents"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                infoLink={`${graphInfoLink}${entity}#days-since-groups-are-failing`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.oldestGroupEvent")}
              />
            </Col100>
          </RowCenter>
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
                infoLink={`${graphInfoLink}${entity}#tags-by-groups`}
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
                documentName={"oldestEvents"}
                documentType={"barChart"}
                entity={entity}
                generatorName={"generic"}
                generatorType={"c3"}
                infoLink={`${graphInfoLink}groups#days-since-group-is-failing`}
                reportMode={reportMode}
                subject={subject}
                title={t("tagIndicator.oldestEvent")}
              />
            </Col100>
          </RowCenter>
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
              <Col100>
                <PanelCollapseHeader>
                  <h1>{t("analytics.sections.forces.title")}</h1>
                </PanelCollapseHeader>
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
                  generatorName={"generic"}
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
                  generatorName={"generic"}
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
                  generatorName={"generic"}
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
    </React.StrictMode>
  );
};
