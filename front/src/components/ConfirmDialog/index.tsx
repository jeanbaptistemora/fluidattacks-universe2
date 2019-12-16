/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that renders the footer
 */

import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import { connect, ConnectedComponent, MapDispatchToProps, MapStateToProps } from "react-redux";
import { Dispatch } from "redux";
import { closeConfirmDialog, IActionStructure } from "../../scenes/Dashboard/actions";
import { IDashboardState } from "../../scenes/Dashboard/reducer";
import translate from "../../utils/translations/translate";
import { Button } from "../Button/index";
import { Modal } from "../Modal/index";

interface IConfirmDialogStateProps {
  isOpen: boolean;
}

interface IConfirmDialogDispatchProps {
  onClose(): void;
}

interface IConfirmDialogBaseProps {
  children?: React.ReactNode;
  closeOnProceed?: boolean;
  message?: string;
  name: string;
  onlyProceed?: boolean;
  title: string;
  onNotProceed?(): void;
  onProceed?(): void;
}

type IConfirmDialogProps = IConfirmDialogBaseProps & (IConfirmDialogStateProps & IConfirmDialogDispatchProps);

export const confirmDialog: React.FC<IConfirmDialogProps> = (props: IConfirmDialogProps): JSX.Element => {
  const handleClose: (() => void) = (): void => {
    if (props.onNotProceed !== undefined) {
      props.onNotProceed();
    }
    props.onClose();
  };
  const handleProceed: (() => void) = (): void => {
    if (props.onProceed !== undefined) {
      props.onProceed();
    }
    if (props.closeOnProceed === true) {
      props.onClose();
    }
  };

  return (
    <React.StrictMode>
      <Modal
        headerTitle={props.title}
        open={props.isOpen}
        footer={
          <ButtonToolbar className="pull-right">
            {props.onlyProceed === undefined ?
              <Button onClick={handleClose}>
                {translate.t("confirmmodal.cancel")}
              </Button> : undefined}
            <Button
              bsStyle="primary"
              onClick={handleProceed}
            >
              {translate.t("confirmmodal.proceed")}
            </Button>
          </ButtonToolbar>
        }
      >
        <Row>
          <Col md={12}>
            <p>{props.message === undefined ? translate.t("confirmmodal.message") : props.message}</p>
            {props.children}
          </Col>
        </Row>
      </Modal>
    </React.StrictMode>
  );
};

confirmDialog.defaultProps = {
  closeOnProceed: true,
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IConfirmDialogStateProps, IConfirmDialogBaseProps, IState> =
  (state: IState, ownProps: IConfirmDialogBaseProps): IConfirmDialogStateProps => {
    const dialogState: { isOpen: boolean } = state.dashboard.confirmDialog[ownProps.name];

    return ({ isOpen: _.isUndefined(dialogState) ? false : dialogState.isOpen });
  };

const mapDispatchToProps: MapDispatchToProps<IConfirmDialogDispatchProps, IConfirmDialogBaseProps> =
  (dispatch: Dispatch, ownProps: IConfirmDialogBaseProps): IConfirmDialogDispatchProps => ({
    onClose: (): IActionStructure => dispatch(closeConfirmDialog(ownProps.name)),
  });

const connectedConfirmDialog: ConnectedComponent<React.FC<IConfirmDialogProps>, IConfirmDialogBaseProps>
  = connect(mapStateToProps, mapDispatchToProps)(confirmDialog);
export { connectedConfirmDialog as ConfirmDialog };
