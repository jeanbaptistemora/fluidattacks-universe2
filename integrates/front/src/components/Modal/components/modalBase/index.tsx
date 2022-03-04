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
  size?: string;
}

const ModalBase: React.FC<IModalProps> = (
  props: Readonly<IModalProps>
): JSX.Element => {
  const { children, headerTitle, size = "" } = props;

  useEffect((): (() => void) => {
    document.body.style.setProperty("overflow", "hidden");

    return function cleanup(): void {
      document.body.style.removeProperty("overflow");
    };
  }, []);

  return (
    <div>
      <ModalContainer>
        <div>
          <ModalDialog className={size}>
            <ModalHeader className={`${size}-title`}>
              <ModalTitle>{headerTitle}</ModalTitle>
            </ModalHeader>
            <ModalBody>{children}</ModalBody>
          </ModalDialog>
        </div>
      </ModalContainer>
    </div>
  );
};

export { ModalBase, IModalProps };
