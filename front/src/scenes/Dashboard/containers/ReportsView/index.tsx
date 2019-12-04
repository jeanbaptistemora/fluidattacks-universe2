import React from "react";
import { Button, Col, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { default as style } from "./index.css";

const reportsView: React.FC<RouteComponentProps> = (props: RouteComponentProps): JSX.Element => {
  const handleDownloadClick: (() => void) = (): void => { window.location.assign("/integrates/complete_report"); };

  return (
    <React.StrictMode>
      <div className={style.container}>
        <Row>
          <Col md={10} sm={8}>
            <h2>Reports</h2>
            <Button onClick={handleDownloadClick}>Download</Button>
          </Col>
        </Row>
      </div>
    </React.StrictMode>
  );
};

export { reportsView as ReportsView };
