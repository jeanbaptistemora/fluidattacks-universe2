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
import translate from "../../../../utils/translations/translate";
import styles from "./index.css";
import { GET_DOCUMENT } from "./queries";
import { ID3GroupIndicatorsProps } from "./types";

const d3GroupIndicatorsView: React.FC<ID3GroupIndicatorsProps> = (props: ID3GroupIndicatorsProps): JSX.Element => {
  const { projectName: groupName } = useParams();

  const {
    data: whereToFindingsData,
    error: whereToFindingsError,
    loading: loadingWhereToFindings,
  } = useQuery(GET_DOCUMENT, {
    variables: {
      documentName: "where_to_findings",
      documentType: "disjoint_force_directed_graph",
      groupName,
    },
  });

  if (loadingWhereToFindings || !_.isEmpty(whereToFindingsError)) {
    return <React.Fragment />;
  }

  const whereToFindings: disjointForceDirectedGraphGeneratorDataType = whereToFindingsData.analytics.groupDocument;

  return (
    <React.StrictMode>
      <Grid>
        <Row>
          <Col xs={2} sm={3} md={4}>
            <Graphic
              bsClass={styles.height160}
              data={whereToFindings}
              footer={translate.t("analytics.disjointForceDirectedGraphGenerator.whereToFindings.footer")}
              generator={disjointForceDirectedGraphGenerator}
              title={translate.t("analytics.disjointForceDirectedGraphGenerator.whereToFindings.title")}
            />
          </Col>
        </Row>
      </Grid>
    </React.StrictMode>
  );
};

export { d3GroupIndicatorsView as D3GroupIndicatorsView };
