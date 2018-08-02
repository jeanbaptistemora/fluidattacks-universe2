// tslint:disable jsx-no-lambda, no-unbound-method
import PropTypes from "prop-types";
import React from "react";
/**
 *  CompulsoryNotice properties
 */
interface IMdlProps {
  btnAcceptText: string;
  id: string;
  rememberText: string;
  text: string;
  title: string;
  onClick(): void;
}
/**
 * CompulsoryNotice component
 */
const compulsoryNotice: React.StatelessComponent<IMdlProps> =
  (props: IMdlProps): JSX.Element => (
  <React.StrictMode>
    <div className="modal-colored-header" id={props.id}>
      <div className="modal-content">
        <div className="modal-header">
          <h3 className="modal-title">{props.title}</h3>
        </div>
        <div className="modal-body">
          <p>{props.text}</p>
          <p>
            <input type="checkbox" id="remember_decision"/>
            {props.rememberText}
          </p>
        </div>
        <div className="modal-footer">
          <button
            className="btn btn-primary"
            onClick={props.onClick}
            type="button"
          >
            {props.btnAcceptText}
          </button>
        </div>
      </div>
    </div>
  </React.StrictMode>
);
/**
 *  CompulsoryNotice propTypes Definition
 */
compulsoryNotice.propTypes = {
  btnAcceptText: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  rememberText: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
};

export = compulsoryNotice;
