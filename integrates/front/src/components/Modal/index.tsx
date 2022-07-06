import { faClose } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useEffect } from "react";
import { createPortal } from "react-dom";

import { ModalConfirm } from "./Confirm";
import { Container as ContainerModal, Dialog, Header, Title } from "./styles";

import { Button } from "components/Button";
import { Container } from "components/Container";

interface IModalProps {
  children: React.ReactNode;
  id?: string;
  minWidth?: number;
  onClose?: () => void;
  open: boolean;
  title: React.ReactNode | string;
}

const Modal: React.FC<IModalProps> = ({
  children,
  id,
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
        <ContainerModal id={id}>
          <Dialog>
            <Header>
              <Title>{title}</Title>
              {onClose ? (
                <Button id={"modal-close"} onClick={onClose} size={"sm"}>
                  <FontAwesomeIcon icon={faClose} />
                </Button>
              ) : undefined}
            </Header>
            <Container minWidth={`${minWidth}px`} padding={"10px"}>
              {children}
            </Container>
          </Dialog>
        </ContainerModal>,
        document.body
      )
    : null;
};

export type { IModalProps };
export { Modal, ModalConfirm };
