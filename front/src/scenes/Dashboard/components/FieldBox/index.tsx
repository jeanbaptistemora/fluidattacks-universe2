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

export = fieldBox;
