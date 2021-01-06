import { Button } from "components/Button";
import { Modal } from "components/Modal";
import React from "react";
import _ from "lodash";
import { translate } from "utils/translations/translate";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";

interface IConfirmFn {
  (confirmCallback: () => void, cancelCallback?: () => void): void;
}

interface IConfirmDialogProps {
  message?: string;
  title: string;
  children: (confirm: IConfirmFn) => React.ReactNode;
}

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
      <Modal headerTitle={title} open={isOpen}>
        {messageLines.map(
          (line: string): JSX.Element => (
            <p key={line}>{line}</p>
          )
        )}
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button id={"confirmmodal-cancel"} onClick={handleClose}>
                {translate.t("confirmmodal.cancel")}
              </Button>
              <Button id={"confirmmodal-proceed"} onClick={handleProceed}>
                {translate.t("confirmmodal.proceed")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </Modal>
      {children(confirm)}
    </React.Fragment>
  );
};

export { IConfirmFn, ConfirmDialog };
