import { Button } from "components/Button";
import { Modal } from "components/Modal";
import React from "react";
import _ from "lodash";
import { translate } from "utils/translations/translate";
import styled, { StyledComponent } from "styled-components";

interface IConfirmFn {
  (confirmCallback: () => void, cancelCallback?: () => void): void;
}

interface IConfirmDialogProps {
  message?: string;
  title: string;
  children: (confirm: IConfirmFn) => React.ReactNode;
}

const StyledToolbar: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "fr",
})``;

const ConfirmDialog: React.FC<IConfirmDialogProps> = (
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

  const confirm: IConfirmFn = (
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
    <React.Fragment>
      <Modal
        footer={
          <StyledToolbar>
            <Button onClick={handleClose}>
              {translate.t("confirmmodal.cancel")}
            </Button>
            <Button onClick={handleProceed}>
              {translate.t("confirmmodal.proceed")}
            </Button>
          </StyledToolbar>
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
    </React.Fragment>
  );
};

export { IConfirmFn, ConfirmDialog };
