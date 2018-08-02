// tslint:disable jsx-no-lambda, no-unbound-method
import PropTypes from "prop-types";
import React from "react";
/**
 *  CompulsoryNotice properties
 */
interface IMdlProps {
  btnAcceptText: string;
  btnAcceptTooltip: string;
  id: string;
  noticeText: string;
  noticeTitle: string;
  rememberText: string;
  rememberTooltip: string;
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
          <h3 className="modal-title">{props.noticeTitle}</h3>
        </div>
        <div className="modal-body">
          <p>{props.noticeText}</p>
          <p title={props.rememberTooltip}>
            <input
              type="checkbox"
              id="remember_decision"
            />
            {props.rememberText}
          </p>
        </div>
        <div className="modal-footer">
          <button
            className="btn btn-primary"
            onClick={props.onClick}
            type="button"
            title={props.btnAcceptTooltip}
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
  btnAcceptTooltip: PropTypes.string,
  id: PropTypes.string.isRequired,
  noticeText: PropTypes.string.isRequired,
  noticeTitle: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  rememberText: PropTypes.string.isRequired,
  rememberTooltip: PropTypes.string,
};

export = compulsoryNotice;
