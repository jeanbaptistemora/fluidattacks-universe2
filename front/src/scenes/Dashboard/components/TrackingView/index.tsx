/* tslint:disable jsx-no-multiline-js
 * Disabling this rule is necessary for the sake of readability
 * of the code that renders the timeline items
 */
import _ from "lodash";
import PropTypes from "prop-types";
import React from "react";
import { Col, Row } from "react-bootstrap";
import TextareaAutosize from "react-textarea-autosize";
import { vulnsView as VulnerabilitiesView } from "../Vulnerabilities/index";
import style from "./index.css";

interface ITrackingViewProps {
  closedFindingsContent?: string;
  closedFindingsTitle: string;
  closings: closing[];
  cycleText: string;
  discoveryDate: string;
  discoveryText: string;
  efectivenessText: string;
  findingId: string;
  hasNewVulnerabilities: boolean;
  openFindingsContent?: string;
  openFindingsTitle: string;
  translations: { [key: string]: string };
}

interface IClosing {
  closed: string;
  cycle: string;
  efectividad: string;
  estado: string;
  finding: string;
  id: string;
  opened: string;
  position: number;
  requested: string;
  timeFormat: string;
  timestamp: string;
  verified: string;
  visibles: string;
  whichClosed: string;
  whichOpened: string;
}

export declare type closing = IClosing;

export const trackingView: React.StatelessComponent<ITrackingViewProps> =
  (props: ITrackingViewProps): JSX.Element => (
    <React.StrictMode>
      <Row>
        { props.hasNewVulnerabilities
          ? <React.Fragment>
            <Col
              md={12}
            >
              <Row>
                <Col
                  md={2}
                  className={style.text_right}
                >
                  <label className={style.track_title}>{props.openFindingsTitle}</label>
                </Col>
                <Col
                  md={10}
                >
                  <VulnerabilitiesView
                    dataInputs={[]}
                    dataLines={[]}
                    dataPorts={[]}
                    editMode={false}
                    findingId={props.findingId}
                    state={"open"}
                    translations={props.translations}
                  />
                </Col>
              </Row>
              <Row>
                <Col
                  md={2}
                  className={style.text_right}
                >
                  <label className={style.track_title}>{props.closedFindingsTitle}</label>
                </Col>
                <Col
                  md={10}
                >
                  <VulnerabilitiesView
                    dataInputs={[]}
                    dataLines={[]}
                    dataPorts={[]}
                    editMode={false}
                    findingId={props.findingId}
                    state={"closed"}
                    translations={props.translations}
                  />
                </Col>
              </Row>
            </Col>
            </React.Fragment>
          : undefined
        }
        {!props.hasNewVulnerabilities && !_.isNil(props.hasNewVulnerabilities)
          ? <React.Fragment>
              <Col
                md={12}
              >
                <p>{props.openFindingsTitle}</p>
                <TextareaAutosize
                  className={style.findingsBox}
                  disabled={true}
                  value={props.openFindingsContent}
                />
              </Col>

                <Col
                  md={12}
                >
                  <p>{props.closedFindingsTitle}</p>
                  <TextareaAutosize
                    className={style.findingsBox}
                    disabled={true}
                    value={props.closedFindingsContent}
                  />
                </Col>
            </React.Fragment>
          : undefined
        }
      </Row>
    </React.StrictMode>
);

trackingView.defaultProps = {
  closings: [],
};

trackingView.propTypes = {
  closedFindingsContent: PropTypes.string,
  closedFindingsTitle: PropTypes.string.isRequired,
  closings: PropTypes.array,
  cycleText: PropTypes.string.isRequired,
  discoveryDate: PropTypes.string.isRequired,
  discoveryText: PropTypes.string.isRequired,
  efectivenessText: PropTypes.string.isRequired,
  hasNewVulnerabilities: PropTypes.bool.isRequired,
  openFindingsContent: PropTypes.string,
  openFindingsTitle: PropTypes.string.isRequired,
};
