import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { Modal, ModalConfirm } from "components/Modal";

interface ICallbackFn {
  (confirmCallback: () => void, cancelCallback: () => void): void;
}

interface IConfirmDialogProps {
  message?: React.ReactNode;
  disable?: boolean;
  title: string;
  children: (callback: ICallbackFn) => React.ReactNode;
  isOpen: boolean;
}

const ConfirmDialog: React.FC<IConfirmDialogProps> = ({
  disable = false,
  children,
  title,
  isOpen,
  message,
}: Readonly<IConfirmDialogProps>): JSX.Element => {
  const { t } = useTranslation();

  const [confirmCallback, setConfirmCallback] = useState(
    (): (() => void) => (): void => undefined
  );
  const [cancelCallback, setCancelCallback] = useState(
    (): (() => void) => (): void => undefined
  );

  const callbacks: ICallbackFn = (
    confirmFn: () => void,
    cancelFn: () => void
  ): void => {
    setConfirmCallback((): (() => void) => confirmFn);
    setCancelCallback((): (() => void) => cancelFn);
  };

  const handleClose = useCallback((): void => {
    cancelCallback();
  }, [cancelCallback]);

  const handleProceed = useCallback((): void => {
    confirmCallback();
  }, [confirmCallback]);

  return (
    <React.Fragment>
      <Modal onClose={handleClose} open={isOpen} title={title}>
        {message}
        <ModalConfirm
          disabled={disable}
          onCancel={handleClose}
          onConfirm={handleProceed}
          txtConfirm={t("searchFindings.tabEvidence.fields.modal.continue")}
        />
      </Modal>
      {children(callbacks)}
    </React.Fragment>
  );
};

export { ConfirmDialog };
