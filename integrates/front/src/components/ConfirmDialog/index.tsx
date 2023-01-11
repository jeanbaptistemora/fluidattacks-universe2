import React, { useCallback, useState } from "react";

import { Modal, ModalConfirm } from "components/Modal";

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

  const handleClose = useCallback((): void => {
    setIsOpen(false);
    cancelCallback();
  }, [cancelCallback]);

  const handleProceed = useCallback((): void => {
    setIsOpen(false);
    confirmCallback();
  }, [confirmCallback]);

  return (
    <React.Fragment>
      <Modal onClose={handleClose} open={isOpen} title={title}>
        {message}
        <ModalConfirm onCancel={handleClose} onConfirm={handleProceed} />
      </Modal>
      {children(confirm)}
    </React.Fragment>
  );
};

export type { IConfirmDialogProps, IConfirmFn };
export { ConfirmDialog };
