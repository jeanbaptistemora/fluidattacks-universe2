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
        <Container width={width}>
          {onClose ? (
            <div className={"tr"}>
              <Button id={"close-filters"} onClick={onClose} size={"sm"}>
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
