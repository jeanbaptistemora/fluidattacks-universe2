import { faClose } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { createPortal } from "react-dom";

import { Container } from "./styles";

import { Button } from "components/Button";

interface ISidePanelProps {
  children: JSX.Element;
  open: boolean;
  onClose?: () => void;
}

const SidePanel = ({
  children,
  open,
  onClose,
}: Readonly<ISidePanelProps>): JSX.Element | null => {
  return open
    ? createPortal(
        <Container>
          {onClose ? (
            <div className={"self-end"}>
              <Button onClick={onClose} size={"sm"}>
                <FontAwesomeIcon icon={faClose} />
              </Button>
            </div>
          ) : undefined}
          {children}
        </Container>,
        document.body
      )
    : null;
};

export type { ISidePanelProps };
export { SidePanel };
