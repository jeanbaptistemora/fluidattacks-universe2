import React from "react";

import type { IModalProps } from "./components/modalBase";
import { ModalBase } from "./components/modalBase";

const Modal: React.FC<IModalProps> = (
  props: Readonly<IModalProps>
): JSX.Element | null => {
  const { children, headerTitle, open, size } = props;

  return open ? (
    <ModalBase headerTitle={headerTitle} open={open} size={size}>
      {children}
    </ModalBase>
  ) : null;
};

export { Modal };
