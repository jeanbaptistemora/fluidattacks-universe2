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
import { StateType } from "typesafe-actions";
import { default as Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import rootReducer from "../../../../store/rootReducer";
import reduxWrapper from "../../../../utils/reduxWrapper";
import {
  acceptLegal,
  setRemember,
} from "../../actions";

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
}

type RootState = StateType<typeof rootReducer>;

const mapStateToProps: any = (state: RootState): any =>
  ({
    open: state.registration.legalNotice.open,
    rememberDecision: state.registration.legalNotice.rememberDecision,
  });

const modalContent: ((arg1: ICompulsoryNoticeProps) => React.ReactNode) =
  (props: ICompulsoryNoticeProps): React.ReactNode => (
  <div>
    <p>{props.noticeText}</p>
    <p title={props.rememberTooltip}>
      <Checkbox
        checked={props.rememberDecision}
        onClick={(): void => { store.dispatch(setRemember(!props.rememberDecision)); }}
      >
        {props.rememberText}
      </Checkbox>
    </p>
  </div>
);

const modalFooter: ((arg1: ICompulsoryNoticeProps) => React.ReactNode) =
  (props: ICompulsoryNoticeProps): React.ReactNode => (
  <Button
    bsStyle="primary"
    title={props.btnAcceptTooltip}
    onClick={(): void => { store.dispatch(acceptLegal(props.rememberDecision)); }}
  >
    {props.btnAcceptText}
  </Button>
);

/**
 * CompulsoryNotice component
 */
export const compulsoryNoticeComponent: React.StatelessComponent<ICompulsoryNoticeProps> =
  (props: ICompulsoryNoticeProps): JSX.Element => (
  <React.StrictMode>
    <Modal
      open={props.open}
      onClose={(): void => { store.dispatch(acceptLegal(props.rememberDecision)); }}
      headerTitle={props.noticeTitle}
      content={modalContent(props)}
      footer={modalFooter(props)}
    />
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
  open: PropTypes.bool.isRequired,
  rememberDecision: PropTypes.bool.isRequired,
  rememberText: PropTypes.string.isRequired,
  rememberTooltip: PropTypes.string,
};

/**
 * Export the Redux-wrapped component
 */
export const compulsoryNotice: React.StatelessComponent<ICompulsoryNoticeProps> = reduxWrapper
(
  compulsoryNoticeComponent,
  mapStateToProps,
);
