import PropTypes from "prop-types";
import React from "react";
import { Col, Row } from "react-bootstrap";
import style from "./index.css";
/**
 * IFrame's properties
 */
interface IFrameProps {
  height: number;
  id: string;
  src: string;
}
/**
 * Frame
 */
const frame: React.FunctionComponent<IFrameProps> =
  (props: IFrameProps): JSX.Element => (
  <React.StrictMode>
    <Row className={style.frame_container}>
      <Col xs={12} md={12} sm={12}>
        <iframe
          id={props.id}
          className={style.frame_content}
          width="100%"
          scrolling="no"
          frameBorder="0"
          height={props.height}
          src={props.src}
        />
      </Col>
    </Row>
  </React.StrictMode>
);
/**
 *  IFrame's propTypes Definition
 */
frame.propTypes = {
  height: PropTypes.number.isRequired,
  id: PropTypes.string.isRequired,
  src: PropTypes.string.isRequired,
};

export = frame;
