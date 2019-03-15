import React from "react";
import { Col, Row } from "react-bootstrap";
import style from "./index.css";

interface ITabItemProps {
  icon: JSX.Element;
  labelText: string;
  onClick(): void;
}

const tabItem: React.SFC<ITabItemProps> = (props: ITabItemProps): JSX.Element => {
  const handleClick: (() => void) = (): void => { props.onClick(); };

  return (
    <React.StrictMode>
      <li className={style.container} onClick={handleClick}>
        <Row>
          <Col md={2}><div className={style.icon}>{props.icon}</div></Col>
          <Col md={10}><span>{props.labelText}</span></Col>
        </Row>
      </li>
    </React.StrictMode>
  );
};

export { tabItem as TabItem };
