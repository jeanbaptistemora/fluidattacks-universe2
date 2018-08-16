/* tslint:disable:jsx-no-lambda no-any
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-ANY: Disabling this rule is necessary because there are no specific types
 * for functions such as mapStateToProps and mapDispatchToProps used in the
 * redux wrapper of this component
 */
import PropTypes from "prop-types";
import React from "react";
import { Button, Checkbox } from "react-bootstrap";
import Modal from "react-responsive-modal";
import { Dispatch } from "redux";
import { StateType } from "typesafe-actions";
import connectWithStore from "../../../../store/connect";
import {
  acceptLegal,
  RegistrationAction,
  setRemember,
} from "../../../../store/Registration/actions";
import rootReducer from "../../../../store/rootReducer";
import style from "./index.css";

/**
 *  CompulsoryNotice properties
 */
interface ICompulsoryNoticeProps {
  btnAcceptText: string;
  btnAcceptTooltip: string;
  id: string;
  noticeText: string;
  noticeTitle: string;
  open: boolean;
  rememberDecision: boolean;
  rememberText: string;
  rememberTooltip: string;
  onAccept(arg1: boolean): void;
  onRememberCheck(arg1: boolean): void;
}

type RootState = StateType<typeof rootReducer>;

const mapStateToProps: any = (state: RootState): any =>
  ({
    open: state.registration.legalNotice.open,
    rememberDecision: state.registration.legalNotice.rememberDecision,
  });

const mapDispatchToProps: any = (dispatch: Dispatch): any =>
  ({
    onAccept: (remember: boolean): RegistrationAction => dispatch(acceptLegal(remember)),
    onRememberCheck: (value: boolean): RegistrationAction => dispatch(setRemember(value)),
  });

/**
 * CompulsoryNotice component
 */
export const compulsoryNoticeComponent: React.StatelessComponent<ICompulsoryNoticeProps> =
  (props: ICompulsoryNoticeProps): JSX.Element => (
  <React.StrictMode>
    <Modal
      open={props.open}
      onClose={(): void => { props.onAccept(props.rememberDecision); }}
      classNames={{ overlay: style.overlay, modal: style.dialog }}
      closeOnEsc={false}
      closeOnOverlayClick={false}
      showCloseIcon={false}
      center={true}
    >
      <div className={style.content} id={props.id}>
        <div className={style.header}>
          <h3 className={style.title}>{props.noticeTitle}</h3>
        </div>
        <div className={style.body}>
          <p>{props.noticeText}</p>
          <p title={props.rememberTooltip}>
            <Checkbox
              checked={props.rememberDecision}
              onClick={(): void => { props.onRememberCheck(!props.rememberDecision); }}
            >
              {props.rememberText}
            </Checkbox>
          </p>
        </div>
        <div className={style.footer}>
          <Button
            bsStyle="primary"
            title={props.btnAcceptTooltip}
            onClick={(): void => { props.onAccept(props.rememberDecision); }}
          >
            {props.btnAcceptText}
          </Button>
        </div>
      </div>
    </Modal>
  </React.StrictMode>
);

/**
 *  CompulsoryNotice propTypes Definition
 */
compulsoryNoticeComponent.propTypes = {
  btnAcceptText: PropTypes.string.isRequired,
  btnAcceptTooltip: PropTypes.string,
  id: PropTypes.string.isRequired,
  noticeText: PropTypes.string.isRequired,
  noticeTitle: PropTypes.string.isRequired,
  onAccept: PropTypes.func.isRequired,
  onRememberCheck: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
  rememberDecision: PropTypes.bool.isRequired,
  rememberText: PropTypes.string.isRequired,
  rememberTooltip: PropTypes.string,
};

/**
 * Export the Redux-wrapped component
 */
export const compulsoryNotice: React.StatelessComponent<ICompulsoryNoticeProps> = connectWithStore
(
  compulsoryNoticeComponent,
  mapStateToProps,
  mapDispatchToProps,
);
