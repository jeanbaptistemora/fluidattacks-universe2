import { faClose } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC, ReactNode } from "react";
import React, { useEffect } from "react";
import { createPortal } from "react-dom";

import { ModalConfirm } from "./Confirm";
import { Container as ContainerModal, Dialog, Header } from "./styles";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Text } from "components/Text";

interface IModalProps {
  children: React.ReactNode;
  id?: string;
  minWidth?: number;
  onClose?: () => void;
  open: boolean;
  title: ReactNode | string;
}

const Modal: FC<IModalProps> = ({
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
              <Text fw={7} mr={2} size={4}>
                {title}
              </Text>
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
