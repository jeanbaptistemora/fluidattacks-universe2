import _ from "lodash";
import React from "react";
import { Col, Grid, Row } from "react-bootstrap";
import { useParams } from "react-router";
import { Graphic } from "../../../../graphics/components/Graphic";
import translate from "../../../../utils/translations/translate";
import styles from "./index.css";
import { ID3GroupIndicatorsProps } from "./types";

const d3GroupIndicatorsView: React.FC<ID3GroupIndicatorsProps> = (props: ID3GroupIndicatorsProps): JSX.Element => {
  const { projectName: groupName } = useParams();

  return (
    <React.StrictMode>
      <Grid fluid={true}>
        <Row>
          <Col md={12}>
            <Graphic
              bsClass={styles.height320}
              documentName="riskOverTime"
              documentType="stackedBarChart"
              entity="group"
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
              subject={groupName}
              title={translate.t("analytics.stackedBarChart.riskOverTime.title")}
            />
          </Col>
        </Row>
        <Row>
          <Col md={6}>
            <Graphic
              bsClass={styles.height160}
              documentName="treatment"
              documentType="pieChart"
              entity="group"
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
              subject={groupName}
              title={translate.t("analytics.pieChart.treatment.title")}
            />
          </Col>
          <Col md={6}>
            <Graphic
              bsClass={styles.height160}
              documentName="status"
              documentType="pieChart"
              entity="group"
              footer={
                <p>{translate.t("analytics.pieChart.status.footer.intro")}</p>
              }
              generatorName="generic"
              generatorType="c3"
              subject={groupName}
              title={translate.t("analytics.pieChart.status.title")}
            />
          </Col>
        </Row>
        <Row>
          <Col md={3}>
            <Graphic
              bsClass={styles.height80}
              documentName="totalFindings"
              documentType="textBox"
              entity="group"
              generatorName="raw"
              generatorType="textBox"
              subject={groupName}
              title={translate.t("analytics.textBox.totalFindings.title")}
            />
          </Col>
          <Col md={3}>
            <Graphic
              bsClass={styles.height80}
              documentName="totalVulnerabilities"
              documentType="textBox"
              entity="group"
              generatorName="raw"
              generatorType="textBox"
              subject={groupName}
              title={translate.t("analytics.textBox.totalVulnerabilities.title")}
            />
          </Col>
          <Col md={3}>
            <Graphic
              bsClass={styles.height80}
              documentName="findingsBeingReattacked"
              documentType="textBox"
              entity="group"
              generatorName="raw"
              generatorType="textBox"
              subject={groupName}
              title={translate.t("analytics.textBox.findingsBeingReattacked.title")}
            />
          </Col>
          <Col md={3}>
            <Graphic
              bsClass={styles.height80}
              documentName="daysSinceLastRemediation"
              documentType="textBox"
              entity="group"
              generatorName="raw"
              generatorType="textBox"
              subject={groupName}
              title={translate.t("analytics.textBox.daysSinceLastRemediation.title")}
            />
          </Col>
        </Row>
        <Row>
          <Col md={3}>
            <Graphic
              bsClass={styles.height80}
              documentName="maxSeverityFound"
              documentType="textBox"
              entity="group"
              generatorName="raw"
              generatorType="textBox"
              subject={groupName}
              title={translate.t("analytics.textBox.maxSeverityFound.title")}
            />
          </Col>
          <Col md={3}>
            <Graphic
              bsClass={styles.height80}
              documentName="maxOpenSeverity"
              documentType="textBox"
              entity="group"
              generatorName="raw"
              generatorType="textBox"
              subject={groupName}
              title={translate.t("analytics.textBox.maxOpenSeverity.title")}
            />
          </Col>
        </Row>
        <Row>
          <Col md={12}>
            <Graphic
              bsClass={styles.height320}
              documentName="whereToFindings"
              documentType="disjointForceDirectedGraph"
              entity="group"
              footer={
                <ul>
                  <li>{translate.t("analytics.disjointForceDirectedGraph.whereToFindings.footer.grey")}</li>
                  <li>{translate.t("analytics.disjointForceDirectedGraph.whereToFindings.footer.redAndGreen")}</li>
                  <li>{translate.t("analytics.disjointForceDirectedGraph.whereToFindings.footer.size")}</li>
                </ul>
              }
              generatorName="whereToFindings"
              generatorType="disjointForceDirectedGraph"
              subject={groupName}
              title={translate.t("analytics.disjointForceDirectedGraph.whereToFindings.title")}
            />
          </Col>
        </Row>
      </Grid>
    </React.StrictMode>
  );
};

export { d3GroupIndicatorsView as D3GroupIndicatorsView };
