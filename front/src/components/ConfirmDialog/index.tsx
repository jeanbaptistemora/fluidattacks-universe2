import _ from "lodash";
import React from "react";
import { ButtonToolbar } from "react-bootstrap";
import translate from "../../utils/translations/translate";
import { Button } from "../Button/index";
import { Modal } from "../Modal/index";

export interface ConfirmFn {
  (confirmCallback: () => void, cancelCallback?: () => void): void;
}

interface IConfirmDialogProps {
  message?: string;
  title: string;
  children: (confirm: ConfirmFn) => React.ReactNode;
}

export const ConfirmDialog: React.FC<IConfirmDialogProps> = (
  props: Readonly<IConfirmDialogProps>
): JSX.Element => {
  const { children, title, message } = props;
  const [isOpen, setOpen] = React.useState(false);
  const [
    confirmCallback,
    setConfirmCallback,
  ] = React.useState((): (() => void) => (): void => undefined);
  const [
    cancelCallback,
    setCancelCallback,
  ] = React.useState((): (() => void) => (): void => undefined);

  const confirm: ConfirmFn = (
    confirmFn: () => void,
    cancelFn?: () => void
  ): void => {
    setOpen(true);
    setConfirmCallback((): (() => void) => confirmFn);
    if (cancelFn !== undefined) {
      setCancelCallback((): (() => void) => cancelFn);
    }
  };

  function handleClose(): void {
    setOpen(false);
    cancelCallback();
  }

  function handleProceed(): void {
    setOpen(false);
    confirmCallback();
  }

  const messageLines: string[] = (_.isUndefined(message)
    ? translate.t("confirmmodal.message")
    : message
  ).split("\n");

  return (
    <>
      <Modal
        footer={
          // We need className to override default styles from react-bootstrap
          // eslint-disable-next-line react/forbid-component-props
          <ButtonToolbar className={"pull-right"}>
            <Button onClick={handleClose}>
              {translate.t("confirmmodal.cancel")}
            </Button>
            <Button onClick={handleProceed}>
              {translate.t("confirmmodal.proceed")}
            </Button>
          </ButtonToolbar>
        }
        headerTitle={title}
        open={isOpen}
      >
        {messageLines.map(
          (line: string): JSX.Element => (
            <p key={line}>{line}</p>
          )
        )}
      </Modal>
      {children(confirm)}
    </>
  );
};
