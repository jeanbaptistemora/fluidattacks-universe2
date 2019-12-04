import React from "react";
import { Col, Row } from "react-bootstrap";
import { default as style } from "./index.css";

interface IProjectBoxProps {
  description: string;
  name: string;
  onClick(projectName: string): void;
}

const projectBox: React.FC<IProjectBoxProps> = (props: IProjectBoxProps): JSX.Element => {
  const handleClick: (() => void) = (): void => { props.onClick(props.name); };

  return (
    <React.StrictMode>
      <div className={style.container} onClick={handleClick}>
        <Row>
          <Col md={12}>
            <p><b>{props.name}</b></p>
          </Col>
        </Row>
        <hr />
        <Row>
          <Col md={12}>
            <p>{props.description}</p>
          </Col>
        </Row>
      </div>
    </React.StrictMode>
  );
};

export { projectBox as ProjectBox };
