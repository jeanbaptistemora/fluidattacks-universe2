import React, { useState } from "react";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
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
      <Modal onClose={handleClose} open={isOpen} size={"small"} title={title}>
        {message}
        <div>
          <div>
            <ModalFooter>
              <Button
                id={"confirmmodal-cancel"}
                onClick={handleClose}
                variant={"secondary"}
              >
                {translate.t("confirmmodal.cancel")}
              </Button>
              <Button
                id={"confirmmodal-proceed"}
                onClick={handleProceed}
                variant={"primary"}
              >
                {translate.t("confirmmodal.proceed")}
              </Button>
            </ModalFooter>
          </div>
        </div>
      </Modal>
      {children(confirm)}
    </React.Fragment>
  );
};

export { IConfirmFn, ConfirmDialog };
