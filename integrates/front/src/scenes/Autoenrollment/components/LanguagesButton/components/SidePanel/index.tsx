import React from "react";
import { createPortal } from "react-dom";

import { Container, ContainerBack } from "./styles";

import { Button } from "components/Button";
import { Text } from "components/Text";

interface ISidePanelProps {
  children: JSX.Element;
  open: boolean;
  onClose?: () => void;
  width?: string;
}

const SidePanel = ({
  children,
  open,
  onClose,
  width = "350px",
}: Readonly<ISidePanelProps>): JSX.Element | null => {
  return open
    ? createPortal(
        <ContainerBack>
          <Container width={width}>
            {onClose ? (
              <div className={"tr"}>
                <Button onClick={onClose} size={"sm"}>
                  <Text bright={6} disp={"inline"} tone={"light"}>
                    {"X Close"}
                  </Text>
                </Button>
              </div>
            ) : undefined}
            {children}
          </Container>
        </ContainerBack>,
        document.body
      )
    : null;
};

export type { ISidePanelProps };
export { SidePanel };
