import React, { useEffect } from "react";
import { createPortal } from "react-dom";

import {
  ModalBody,
  ModalContainer,
  ModalDialog,
  ModalHeader,
  ModalTitle,
} from "./styles";

interface IModalProps {
  children: React.ReactNode;
  headerTitle: React.ReactNode | string;
  onClose?: () => void;
  open: boolean;
}

const Modal: React.FC<IModalProps> = ({
  children,
  headerTitle,
  onClose,
  open,
}: IModalProps): JSX.Element | null => {
  useEffect((): (() => void) => {
    const handleKeydown = (event: KeyboardEvent): void => {
      if (event.key === "Escape" && onClose !== undefined) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeydown);

    return (): void => {
      window.removeEventListener("keydown", handleKeydown);
    };
  }, [onClose]);

  return open
    ? createPortal(
        <ModalContainer>
          <ModalDialog>
            <ModalHeader>
              <ModalTitle>{headerTitle}</ModalTitle>
            </ModalHeader>
            <ModalBody>{children}</ModalBody>
          </ModalDialog>
        </ModalContainer>,
        document.body
      )
    : null;
};

export { Modal };
