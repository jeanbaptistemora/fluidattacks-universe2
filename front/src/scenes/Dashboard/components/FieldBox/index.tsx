/* tslint:disable jsx-no-multiline-js
 * Disabling this rule is necessary for the sake of readability
 * of the code that renders/hides the component
 */
import PropTypes from "prop-types";
import React from "react";
import { Col } from "react-bootstrap";

interface IFieldBoxProps {
  content: string;
  title: string;
}

const fieldBox: React.FunctionComponent<IFieldBoxProps> =
  (props: IFieldBoxProps): JSX.Element => (
    <React.StrictMode>
      <div className="row table-row">
        <Col xs={12} md={4}>
          <div className="table-head">
            <label><b>{props.title}</b></label>
          </div>
        </Col>
        <Col xs={12} md={8}>
          <p>
            {props.content}
          </p>
        </Col>
      </div>
    </React.StrictMode>
  );

fieldBox.propTypes = {
  content: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
};

export = fieldBox;
