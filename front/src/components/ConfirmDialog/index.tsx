/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that renders the footer
 */

import _ from "lodash";
import React from "react";
import { Button, ButtonToolbar, Col, Row } from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { Dispatch } from "redux";
import { closeConfirmDialog, IActionStructure } from "../../scenes/Dashboard/actions";
import { IDashboardState } from "../../scenes/Dashboard/reducer";
import translate from "../../utils/translations/translate";
import { default as Modal } from "../Modal/index";

interface IConfirmDialogStateProps {
  isOpen: boolean;
}

interface IConfirmDialogDispatchProps {
  onClose(): void;
}

interface IConfirmDialogBaseProps {
  children?: React.ReactNode;
  name: string;
  title: string;
  onProceed(): void;
}

type IConfirmDialogProps = IConfirmDialogBaseProps & (IConfirmDialogStateProps & IConfirmDialogDispatchProps);

const confirmDialog: React.SFC<IConfirmDialogProps> = (props: IConfirmDialogProps): JSX.Element => {
  const handleClose: (() => void) = (): void => { props.onClose(); };
  const handleProceed: (() => void) = (): void => { props.onProceed(); props.onClose(); };

  return (
    <React.StrictMode>
      <Modal
        headerTitle={props.title}
        open={props.isOpen}
        footer={
          <ButtonToolbar className="pull-right">
            <Button onClick={handleClose}>
              {translate.t("confirmmodal.cancel")}
            </Button>
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
            <p>{translate.t("confirmmodal.message")}</p>
            {props.children}
          </Col>
        </Row>
      </Modal>
    </React.StrictMode>
  );
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

export = connect(mapStateToProps, mapDispatchToProps)(confirmDialog);
