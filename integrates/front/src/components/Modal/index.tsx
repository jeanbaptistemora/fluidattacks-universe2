import React, { useEffect } from "react";
import { createPortal } from "react-dom";

import { ModalFooter } from "./Footer";
import { CloseButton, Container, Dialog, Header, Title } from "./styles";

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
            <Header>
              <Title>{headerTitle}</Title>
              {onClose === undefined ? undefined : (
                <CloseButton onClick={onClose}>{"×"}</CloseButton>
              )}
            </Header>
            {children}
          </Dialog>
        </Container>,
        document.body
      )
    : null;
};

export { Modal, ModalFooter };
