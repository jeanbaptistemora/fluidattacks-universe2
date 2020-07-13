import _ from "lodash";
import React from "react";
import { Button, ButtonGroup, Col, Glyphicon, Grid, Panel, Row } from "react-bootstrap";
import translate from "../../../../../../utils/translations/translate";
import styles from "../../index.css";
import { IChartsGenericViewProps } from "../../types";

const chartsGenericViewExtras: React.FC<IChartsGenericViewProps> = (props: IChartsGenericViewProps): JSX.Element => {
  const { entity, subject } = props;

  const downloadPngUrl: URL = new URL(`/integrates/graphics-for-${entity}`, window.location.origin);
  downloadPngUrl.searchParams.set(entity, subject);
  downloadPngUrl.searchParams.set("reportMode", "true");

  return (
    <React.StrictMode>
      <Grid fluid={true}>
        <Row>
          <Col md={12}>
            <Panel>
              <Panel.Heading>
                <Panel.Title>
                  <h1 className={styles.centerTitle}>
                    {translate.t("analytics.sections.extras.title")}
                  </h1>
                </Panel.Title>
              </Panel.Heading>
              <Panel.Body>
                <ButtonGroup>
                  <Button
                    bsSize="large"
                    download={`charts-${entity}-${subject}.png`}
                    href={downloadPngUrl.toString()}
                  >
                    <Glyphicon glyph="save" /> {translate.t("analytics.sections.extras.download")}
                  </Button>
                </ButtonGroup>
              </Panel.Body>
            </Panel>
          </Col>
        </Row>
        <div className={styles.separatorTitleFromCharts} />
      </Grid>
    </React.StrictMode>
  );
};

export { chartsGenericViewExtras as ChartsGenericViewExtras };
