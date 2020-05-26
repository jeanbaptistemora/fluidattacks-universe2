/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that renders the footer
 */

import _ from "lodash";
import React from "react";
import { ButtonToolbar } from "react-bootstrap";
import translate from "../../utils/translations/translate";
import { Button } from "../Button/index";
import { Modal } from "../Modal/index";

export type ConfirmFn = (confirmCallback: () => void, cancelCallback?: () => void) => void;

interface IConfirmDialogProps {
  message?: string;
  title: string;
  children(confirm: ConfirmFn): React.ReactNode;
}

export const confirmDialog: React.FC<IConfirmDialogProps> = (props: IConfirmDialogProps): JSX.Element => {
  const [isOpen, setOpen] = React.useState(false);
  const [confirmCallback, setConfirmCallback] = React.useState(() => (): void => undefined);
  const [cancelCallback, setCancelCallback] = React.useState(() => (): void => undefined);

  const confirm: ConfirmFn = (confirmFn: () => void, cancelFn?: () => void): void => {
    setOpen(true);
    setConfirmCallback(() => confirmFn);
    if (cancelFn !== undefined) {
      setCancelCallback(() => cancelFn);
    }
  };

  const handleClose: (() => void) = (): void => {
    setOpen(false);
    cancelCallback();
  };

  const handleProceed: (() => void) = (): void => {
    setOpen(false);
    confirmCallback();
  };

  const message: string = _.isUndefined(props.message) ? translate.t("confirmmodal.message") : props.message;
  const messageLines: string[] = message.split("\n");

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
        {messageLines.map((line: string) => <p key={line}>{line}</p>)}
      </Modal>
      {props.children(confirm)}
    </React.StrictMode>
  );
};

export { confirmDialog as ConfirmDialog };
