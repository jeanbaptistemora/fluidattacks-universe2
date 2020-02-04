/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that renders the footer
 */

import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import translate from "../../utils/translations/translate";
import { Button } from "../Button/index";
import { Modal } from "../Modal/index";

export type ConfirmFn = (callback: () => void) => void;

interface IConfirmDialogProps {
  message?: string;
  title: string;
  children(confirm: ConfirmFn): React.ReactNode;
}

export const confirmDialog: React.FC<IConfirmDialogProps> = (props: IConfirmDialogProps): JSX.Element => {
  const [isOpen, setOpen] = React.useState(false);
  const [callback, setCallback] = React.useState(() => (): void => undefined);

  const confirm: (callbackFn: () => void) => void = (callbackFn: () => void): void => {
    setOpen(true);
    setCallback(() => callbackFn);
  };

  const handleClose: (() => void) = (): void => {
    setOpen(false);
  };

  const handleProceed: (() => void) = (): void => {
    setOpen(false);
    callback();
  };

  return (
    <React.StrictMode>
      <Modal
        headerTitle={props.title}
        open={isOpen}
        footer={
          <ButtonToolbar className="pull-right">
            <Button onClick={handleClose}>{translate.t("confirmmodal.cancel")}</Button>
            <Button onClick={handleProceed}>{translate.t("confirmmodal.proceed")}</Button>
          </ButtonToolbar>
        }
      >
        <Row>
          <Col md={12}>
            <p>{props.message === undefined ? translate.t("confirmmodal.message") : props.message}</p>
          </Col>
        </Row>
      </Modal>
      {props.children(confirm)}
    </React.StrictMode>
  );
};

export { confirmDialog as ConfirmDialog };
