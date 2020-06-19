import { useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { Graphic } from "../../../../graphics/components/Graphic";
import {
  dataType as disjointForceDirectedGraphGeneratorDataType,
  disjointForceDirectedGraphGenerator,
} from "../../../../graphics/generators/disjointForceDirectedGraph";
import styles from "./index.css";
import { GET_DOCUMENT } from "./queries";
import { ID3GroupIndicatorsProps } from "./types";

const d3GroupIndicatorsView: React.FC<ID3GroupIndicatorsProps> = (props: ID3GroupIndicatorsProps): JSX.Element => {
  const groupName: string = props.groupName;

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
      <Row>
        <Col md={12} sm={12} xs={12}>
          <Row>
            <Col md={8} sm={12} xs={12}>
              <Col md={6} sm={12} xs={12}>
                <Graphic
                  bsClass={styles.height160}
                  data={whereToFindings}
                  generator={disjointForceDirectedGraphGenerator}
                />
              </Col>
            </Col>
          </Row>
        </Col>
      </Row>
    </React.StrictMode>
  );
};

export { d3GroupIndicatorsView as D3GroupIndicatorsView };
