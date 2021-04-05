/* eslint-disable react/forbid-component-props */
import React, { useEffect } from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import style from "./index.css";

import { ModalBody, ModalHeader, ModalTitle } from "styles/styledComponents";

interface IModalProps {
  children: React.ReactNode;
  headerTitle: React.ReactNode | string;
  open: boolean;
  size?: string;
}

const StyledBgModal: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `fixed absolute--fill z-9999 ${style.bgModal}`,
})``;

const StyledModalContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: "fixed absolute--fill overflow-hidden overflow-y-auto pa3 z-9999",
})``;

const StyledModalDialog: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `flex v-mid center relative ma5 ${style.modalDialog}`,
})``;

const StyledModal: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `relative tl outline-0 w-100 ${style.modal}`,
})``;

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
    <React.Fragment>
      <StyledBgModal />
      <StyledModalContainer>
        <StyledModalDialog className={size}>
          <StyledModal>
            <ModalHeader className={`${size}-title`}>
              <ModalTitle>{headerTitle}</ModalTitle>
            </ModalHeader>
            <ModalBody>{children}</ModalBody>
          </StyledModal>
        </StyledModalDialog>
      </StyledModalContainer>
    </React.Fragment>
  );
};

export { ModalBase, IModalProps };
