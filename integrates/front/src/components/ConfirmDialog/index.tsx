import React, { useState } from "react";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

interface IConfirmFn {
  (confirmCallback: () => void, cancelCallback?: () => void): void;
}

interface IConfirmDialogProps {
  message?: React.ReactNode;
  title: string;
  children: (confirm: IConfirmFn) => React.ReactNode;
}

const ConfirmDialog: React.FC<IConfirmDialogProps> = (
  props: Readonly<IConfirmDialogProps>
): JSX.Element => {
  const { children, title, message } = props;
  const [isOpen, setOpen] = useState(false);
  const [confirmCallback, setConfirmCallback] = useState(
    (): (() => void) => (): void => undefined
  );
  const [cancelCallback, setCancelCallback] = useState(
    (): (() => void) => (): void => undefined
  );

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

  return (
    <React.Fragment>
      <Modal headerTitle={title} onEsc={handleClose} open={isOpen}>
        {message}
        <hr />
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
