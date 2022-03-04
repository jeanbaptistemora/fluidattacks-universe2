/* eslint-disable react/forbid-component-props */
import React, { useEffect } from "react";

import {
  ModalBody,
  ModalContainer,
  ModalDialog,
  ModalHeader,
  ModalTitle,
} from "../styles";

interface IModalProps {
  children: React.ReactNode;
  headerTitle: React.ReactNode | string;
  onEsc?: () => void;
  open: boolean;
}

const ModalBase: React.FC<IModalProps> = (
  props: Readonly<IModalProps>
): JSX.Element => {
  const { children, headerTitle } = props;

  useEffect((): (() => void) => {
    document.body.style.setProperty("overflow", "hidden");

    return function cleanup(): void {
      document.body.style.removeProperty("overflow");
    };
  }, []);

  return (
    <ModalContainer>
      <ModalDialog>
        <ModalHeader>
          <ModalTitle>{headerTitle}</ModalTitle>
        </ModalHeader>
        <ModalBody>{children}</ModalBody>
      </ModalDialog>
    </ModalContainer>
  );
};

export { ModalBase, IModalProps };
