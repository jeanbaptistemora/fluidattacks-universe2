import PropTypes from "prop-types";
import React from "react";
import style from "./index.css";
/**
 * Indicator's Box properties
 */
interface IBoxProps {
  backgroundColor: string;
  color: string;
  icon: string;
  name: string;
  quantity: string;
  title: string;
}
/**
 * Project Indicator Box
 */
const indicatorBox: React.StatelessComponent<IBoxProps> =
  (props: IBoxProps): JSX.Element => (
  <React.StrictMode>
    <div className="col-md-3 col-xs-12">
      <div
        className={style.widgetbox}
        data-toggle="tooltip"
        data-placement="top"
        title={props.title}
        style={{backgroundColor: props.backgroundColor, color: props.color}}
      >
        <div className="col-md-4 col-xs-4">
          <div className={style.widgeticon}>
              <span className={props.icon}/>
          </div>
        </div>
        <div className="col-md-8 col-xs-8">
          <div
            data-toggle="counter"
            className={style.widgetvalue}
          >
            {props.quantity}
          </div>
          <div className={style.widgetdesc}>
            {props.name}
          </div>
        </div>
      </div>
    </div>
  </React.StrictMode>
);
/**
 *  Indicator's Box propTypes Definition
 */
indicatorBox.propTypes = {
  backgroundColor: PropTypes.string.isRequired,
  color: PropTypes.string.isRequired,
  icon: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  quantity: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
};

export = indicatorBox;
