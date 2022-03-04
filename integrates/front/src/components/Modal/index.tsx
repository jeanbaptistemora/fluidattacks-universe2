import React, { useEffect } from "react";
import { createPortal } from "react-dom";

import type { IModalProps } from "./components/modalBase";
import { ModalBase } from "./components/modalBase";

const Modal: React.FC<IModalProps> = ({
  children,
  headerTitle,
  onEsc,
  open,
  size,
}: IModalProps): JSX.Element | null => {
  useEffect((): (() => void) => {
    const handleKeydown = (event: KeyboardEvent): void => {
      if (event.key === "Escape" && typeof onEsc === "function") {
        onEsc();
      }
    };
    window.addEventListener("keydown", handleKeydown);

    return (): void => {
      window.removeEventListener("keydown", handleKeydown);
    };
  }, [onEsc]);

  return open
    ? createPortal(
        <ModalBase headerTitle={headerTitle} open={open} size={size}>
          {children}
        </ModalBase>,
        document.body
      )
    : null;
};

export { Modal };
