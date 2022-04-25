import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";

interface IConfirmFn {
  (confirmCallback: () => void, cancelCallback?: () => void): void;
}

interface IConfirmDialogProps {
  message?: React.ReactNode;
  title: string;
  children: (confirm: IConfirmFn) => React.ReactNode;
}

const ConfirmDialog: React.FC<IConfirmDialogProps> = ({
  children,
  title,
  message,
}: Readonly<IConfirmDialogProps>): JSX.Element => {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
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
    setIsOpen(true);
    setConfirmCallback((): (() => void) => confirmFn);
    if (cancelFn !== undefined) {
      setCancelCallback((): (() => void) => cancelFn);
    }
  };

  function handleClose(): void {
    setIsOpen(false);
    cancelCallback();
  }

  function handleProceed(): void {
    setIsOpen(false);
    confirmCallback();
  }

  return (
    <React.Fragment>
      <Modal onClose={handleClose} open={isOpen} size={"small"} title={title}>
        {message}
        <ModalFooter>
          <Button
            id={"confirmmodal-cancel"}
            onClick={handleClose}
            variant={"secondary"}
          >
            {t("confirmmodal.cancel")}
          </Button>
          <Button
            id={"confirmmodal-proceed"}
            onClick={handleProceed}
            variant={"primary"}
          >
            {t("confirmmodal.proceed")}
          </Button>
        </ModalFooter>
      </Modal>
      {children(confirm)}
    </React.Fragment>
  );
};

export type { IConfirmDialogProps, IConfirmFn };
export { ConfirmDialog };
