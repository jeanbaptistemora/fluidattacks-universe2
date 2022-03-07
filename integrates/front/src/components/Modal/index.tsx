import React, { useEffect } from "react";
import { createPortal } from "react-dom";

import { ModalBody } from "./Body";
import { ModalFooter } from "./Footer";
import { ModalHeader } from "./Header";
import { Container, Dialog } from "./styles";
import { ModalTitle } from "./Title";

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
        <Container>
          <Dialog>
            <ModalHeader>
              <ModalTitle>{headerTitle}</ModalTitle>
            </ModalHeader>
            <ModalBody>{children}</ModalBody>
          </Dialog>
        </Container>,
        document.body
      )
    : null;
};

export { Modal, ModalBody, ModalFooter, ModalHeader, ModalTitle };
