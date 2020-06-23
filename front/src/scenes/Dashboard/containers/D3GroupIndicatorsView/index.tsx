import { useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import React from "react";
import { Col, Grid, Row } from "react-bootstrap";
import { useParams } from "react-router";
import { Graphic } from "../../../../graphics/components/Graphic";
import {
  dataType as disjointForceDirectedGraphGeneratorDataType,
  disjointForceDirectedGraphGenerator,
} from "../../../../graphics/generators/disjointForceDirectedGraph";
import {
  dataType as divergingStackedBarChartDataType,
  divergingStackedBarChartGenerator,
} from "../../../../graphics/generators/divergingStackedBarChart";
import translate from "../../../../utils/translations/translate";
import styles from "./index.css";
import { GET_DOCUMENT } from "./queries";
import { ID3GroupIndicatorsProps } from "./types";

const d3GroupIndicatorsView: React.FC<ID3GroupIndicatorsProps> = (props: ID3GroupIndicatorsProps): JSX.Element => {
  const { projectName: groupName } = useParams();

  const { data, error, loading } = useQuery(GET_DOCUMENT, {
    variables: {
      groupName,
      riskOverTimeDocumentName: "risk_over_time",
      riskOverTimeDocumentType: "diverging_stacked_bar_chart",
      whereToFindingsDocumentName: "where_to_findings",
      whereToFindingsDocumentType: "disjoint_force_directed_graph",
    },
  });

  if (loading || !_.isEmpty(error)) {
    return <React.Fragment />;
  }

  const riskOverTime: divergingStackedBarChartDataType = data.riskOverTime.document;
  const whereToFindings: disjointForceDirectedGraphGeneratorDataType = data.whereToFindings.document;

  return (
    <React.StrictMode>
      <Grid>
        <Row>
          <Col xs={6} sm={8} md={10}>
            <Graphic
              bsClass={styles.height320}
              data={riskOverTime}
              generator={divergingStackedBarChartGenerator}
              title={translate.t("analytics.divergingStackedBarChart.riskOverTime.title")}
            />
          </Col>
        </Row>
        <Row>
          <Col xs={3} sm={4} md={5}>
            <Graphic
              bsClass={styles.height160}
              data={whereToFindings}
              footer={
                <ul>
                  <li>{translate.t("analytics.disjointForceDirectedGraph.whereToFindings.footer.grey")}</li>
                  <li>{translate.t("analytics.disjointForceDirectedGraph.whereToFindings.footer.redAndGreen")}</li>
                </ul>
              }
              generator={disjointForceDirectedGraphGenerator}
              title={translate.t("analytics.disjointForceDirectedGraph.whereToFindings.title")}
            />
          </Col>
        </Row>
      </Grid>
    </React.StrictMode>
  );
};

export { d3GroupIndicatorsView as D3GroupIndicatorsView };
