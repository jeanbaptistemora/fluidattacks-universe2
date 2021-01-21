import React from "react";
import type { StyledComponent } from "styled-components";
import style from "./index.css";
import styled from "styled-components";

import { ModalBody, ModalHeader, ModalTitle } from "styles/styledComponents";

interface IModalProps {
  children: React.ReactNode;
  headerTitle: string;
  open: boolean;
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
  className: `relative tl outline-0 ${style.modal}`,
})``;

const Modal: React.FC<IModalProps> = (
  props: Readonly<IModalProps>
): JSX.Element => {
  const { children, headerTitle, open } = props;

  React.useEffect((): (() => void) => {
    if (open) {
      document.body.style.setProperty("overflow", "hidden");
    } else {
      document.body.style.removeProperty("overflow");
    }

    return function cleanup(): void {
      document.body.style.removeProperty("overflow");
    };
  }, [open]);

  return (
    <div>
      {open ? (
        <React.Fragment>
          <StyledBgModal />
          <StyledModalContainer>
            <StyledModalDialog>
              <StyledModal>
                <ModalHeader>
                  <ModalTitle>{headerTitle}</ModalTitle>
                </ModalHeader>
                <ModalBody>{children}</ModalBody>
              </StyledModal>
            </StyledModalDialog>
          </StyledModalContainer>
        </React.Fragment>
      ) : undefined}
    </div>
  );
};

export { Modal };
