import React from "react";

import type { IModalProps } from "./components/modalBase";
import { ModalBase } from "./components/modalBase";

const Modal: React.FC<IModalProps> = (
  props: Readonly<IModalProps>
): JSX.Element | null => {
  const { children, headerTitle, onEsc, open, size } = props;

  window.addEventListener("keydown", (event): void => {
    if (event.key === "Escape" && typeof onEsc === "function") {
      onEsc();
    }
  });

  return open ? (
    <ModalBase headerTitle={headerTitle} open={open} size={size}>
      {children}
    </ModalBase>
  ) : null;
};

export { Modal };
