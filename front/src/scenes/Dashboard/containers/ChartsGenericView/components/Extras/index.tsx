import _ from "lodash";
import React from "react";
import {
  ButtonToolbar,
  Col,
  Glyphicon,
  Grid,
  Panel,
  Row,
} from "react-bootstrap";
import { Button } from "../../../../../../components/Button";
import translate from "../../../../../../utils/translations/translate";
import styles from "../../index.css";
import { IChartsGenericViewProps } from "../../types";

const chartsGenericViewExtras: React.FC<IChartsGenericViewProps> = (props: IChartsGenericViewProps): JSX.Element => {
  const { entity, subject } = props;

  const downloadPngUrl: URL = new URL("/integrates/graphics-report", window.location.origin);
  downloadPngUrl.searchParams.set("entity", entity);
  downloadPngUrl.searchParams.set(entity, subject);

  return (
    <React.StrictMode>
      <Grid fluid={true}>
        <Row>
          <Col md={12}>
            <Panel>
              <Panel.Body>
                <Grid fluid={true}>
                  <Row>
                    <Col mdOffset={0} md={3}>
                      <ButtonToolbar justified={true}>
                        <Button
                          bsSize="large"
                          download={`charts-${entity}-${subject}.png`}
                          href={downloadPngUrl.toString()}
                        >
                          <Glyphicon glyph="save" /> {translate.t("analytics.sections.extras.download")}
                        </Button>
                      </ButtonToolbar>
                    </Col>
                  </Row>
                </Grid>
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
