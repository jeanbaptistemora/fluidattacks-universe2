/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically creates the columns
 */
import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { FluidIcon } from "../../../../components/FluidIcon/index";
import style from "./index.css";
/**
 * Indicator's Box properties
 */
interface IBoxProps {
  icon: string;
  name: string;
  quantity: string;
  title: string;
  total?: string;
}
/**
 * Project Indicator Box
 */
const indicatorBox: React.StatelessComponent<IBoxProps> =
  (props: IBoxProps): JSX.Element => (
  <React.StrictMode>
    <Col xs={12} md={3} sm={4}>
      <div
        className={style.widgetbox}
        data-toggle="tooltip"
        data-placement="top"
        title={props.title}
      >
        <Row>
          <Col xs={2} md={2}>
            <FluidIcon icon={props.icon} width="30px" height="30px" />
          </Col>
          <Col xs={10} md={10}>
            <div className={style.widgetdesc}>
              {props.name}
            </div>
          </Col>
        </Row>
        <hr />
        <Row>
          <div data-toggle="counter" className={style.widgetvalue}>
            { _.isUndefined(props.total)
              ? <React.Fragment>
                  {props.quantity}
                </React.Fragment>
              : <React.Fragment>
                  {props.quantity} <sup>{props.total}</sup>
                </React.Fragment>
            }
          </div>
        </Row>
      </div>
    </Col>
  </React.StrictMode>
);

indicatorBox.defaultProps = {
  icon: "",
  name: "",
  quantity: "",
  title: "",
  total: "",
};

export = indicatorBox;
