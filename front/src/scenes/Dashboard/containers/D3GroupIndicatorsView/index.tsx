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
      <Grid>
        <Row>
          <Col xs={6} sm={8} md={10}>
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
          <Col xs={3} sm={4} md={5}>
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
          <Col xs={3} sm={4} md={5}>
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
          <Col xs={6} sm={8} md={10}>
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
