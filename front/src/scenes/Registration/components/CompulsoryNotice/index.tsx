// tslint:disable jsx-no-lambda, no-unbound-method
import PropTypes from "prop-types";
import React from "react";
import { Button } from "react-bootstrap";
import style from "../../../../components/Modal/index.css";
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
  onAccept(): void;
}
/**
 * CompulsoryNotice component
 */
const compulsoryNotice: React.StatelessComponent<IMdlProps> =
  (props: IMdlProps): JSX.Element => (
  <React.StrictMode>
    <div className={style.modalcontent} id={props.id}>
      <div className={style.modalheader}>
        <h3 className={style.modaltitle}>{props.noticeTitle}</h3>
      </div>
      <div className={style.modalbody}>
        <p>{props.noticeText}</p>
        <p title={props.rememberTooltip}>
          <input
            type="checkbox"
            id="remember_decision"
          />
          {props.rememberText}
        </p>
      </div>
      <div className={style.modalfooter}>
        <Button
          bsStyle="primary"
          title={props.btnAcceptTooltip}
          onClick={props.onAccept}
        >
          {props.btnAcceptText}
        </Button>
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
  onAccept: PropTypes.func.isRequired,
  rememberText: PropTypes.string.isRequired,
  rememberTooltip: PropTypes.string,
};

export = compulsoryNotice;
