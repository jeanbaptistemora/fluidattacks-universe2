/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically creates the columns
 */
import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { FluidIcon } from "../../../../components/FluidIcon/index";
import { default as style } from "./index.css";
/**
 * Indicator's Box properties
 */
interface IBoxProps {
  description?: string;
  icon: string;
  name: string;
  quantity: number | string;
  small?: boolean;
  title: string;
  total?: string;
  onClick?(): void;
}
/**
 * Project Indicator Box
 */
const indicatorBox: React.FunctionComponent<IBoxProps> =
  (props: IBoxProps): JSX.Element => {
    const useSmallStyle: boolean = _.isUndefined(props.small) ? false : props.small;

    const handleClick: (() => void) = (): void => {
      if (props.onClick !== undefined) {
          props.onClick();
      }
    };

    return (
     <React.StrictMode>
        <div
            className={style.widgetbox}
            data-toggle="tooltip"
            data-placement="top"
            title={props.title}
            onClick={handleClick}
        >
            <Row>
            <Col xs={2} md={2}>
                <FluidIcon icon={props.icon} width="30px" height="30px"/>
            </Col>
            <Col xs={10} md={10}>
                <div className={style.widgetdesc} >
                {props.name}
                </div>
            </Col>
            </Row>
            <hr />
            <Row>
            <div
              data-toggle="counter"
              className={useSmallStyle ? style.widgetvaluesmall : style.widgetvalue}
            >
                { _.isUndefined(props.total)
                ? <React.Fragment>
                    {props.quantity}
                    </React.Fragment>
                : <React.Fragment>
                    {props.quantity} <sup>{props.total}</sup>
                    </React.Fragment>
                }
                <br />
                { _.isUndefined(props.description)
                ? <React.Fragment />
                : <React.Fragment>
                    <span className={style.widgetdescription}>
                      {props.description}
                    </span>
                  </React.Fragment>
                }
            </div>
            </Row>
        </div>
    </React.StrictMode>
    );
};

indicatorBox.defaultProps = {
  icon: "",
  name: "",
  quantity: 0,
  title: "",
  total: "",
};

export { indicatorBox as IndicatorBox };
