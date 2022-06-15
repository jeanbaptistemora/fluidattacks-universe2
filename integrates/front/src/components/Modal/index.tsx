import { faClose } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useEffect } from "react";
import { createPortal } from "react-dom";

import { ModalConfirm } from "./Confirm";
import { ModalFooter } from "./Footer";
import { Container, Dialog, Header, Title } from "./styles";

import { ButtonOpacity } from "components/Button";
import { ScrollContainer } from "components/ScrollContainer";

interface IModalProps {
  children: React.ReactNode;
  minWidth?: number;
  onClose?: () => void;
  open: boolean;
  title: React.ReactNode | string;
}

const Modal: React.FC<IModalProps> = ({
  children,
  minWidth = 300,
  title,
  onClose,
  open,
}: IModalProps): JSX.Element | null => {
  useEffect((): (() => void) => {
    const handleKeydown = (event: KeyboardEvent): void => {
      if (event.key === "Escape") {
        onClose?.();
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
          <Dialog minWidth={minWidth}>
            <Header>
              <Title>{title}</Title>
              {onClose ? (
                <ButtonOpacity id={"modal-close"} onClick={onClose}>
                  <FontAwesomeIcon icon={faClose} />
                </ButtonOpacity>
              ) : undefined}
            </Header>
            <ScrollContainer>{children}</ScrollContainer>
          </Dialog>
        </Container>,
        document.body
      )
    : null;
};

export type { IModalProps };
export { Modal, ModalConfirm, ModalFooter };
