/* tslint:disable jsx-no-multiline-js
 * Disabling this rule is necessary for the sake of readability
 * of the code that renders the timeline items
 */
import PropTypes from "prop-types";
import React from "react";
import { Col, Row } from "react-bootstrap";
import TextareaAutosize from "react-textarea-autosize";
import style from "./index.css";

interface ITrackingViewProps {
  closedFindingsContent?: string;
  closedFindingsTitle: string;
  closings: closing[];
  cycleText: string;
  discoveryDate: string;
  discoveryText: string;
  efectivenessText: string;
  openFindingsContent?: string;
  openFindingsTitle: string;
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
      </Row>
      <br/>
      <Row>
        <Col
          mdOffset={3}
          md={9}
          sm={12}
        >
          <ul className={style.timelineContainer}>
            <li key={0} className={style.timelineItem}>
              <div className={style.timelineDate}>
                <span>
                  {props.discoveryDate}
                </span>
              </div>
              <div className={style.timelineContent}>
                  <p>{props.discoveryText}</p>
              </div>
            </li>
            {props.closings.map((item: closing) =>
              <li key={item.cycle} className={style.timelineItem}>
                <div className={style.timelineDate}>
                  <span>
                    {item.timeFormat}
                  </span>
                </div>
                <div className={style.timelineContent}>
                    <p>
                      {props.cycleText}: {item.cycle},
                       {props.openFindingsTitle}: {item.opened},
                       {props.closedFindingsTitle}: {item.closed},
                       {props.efectivenessText}: {item.efectividad}%
                    </p>
                </div>
              </li>,
            )}
          </ul>
        </Col>
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
  openFindingsContent: PropTypes.string,
  openFindingsTitle: PropTypes.string.isRequired,
};
