/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap
*/
import React from "react";
import { Modal, Sizes } from "react-bootstrap";
import { default as style } from "./index.css";

export interface IModalProps {
  bsSize?: Sizes;
  children?: React.ReactNode;
  content?: React.ReactNode;
  footer: React.ReactNode;
  headerTitle: string;
  open: boolean;
  onClose?: () => void;
}

const modal: React.FC<IModalProps> = (
  props: Readonly<IModalProps>
): JSX.Element => {
  const {
    bsSize,
    open,
    headerTitle,
    content,
    children,
    footer,
    onClose,
  } = props;

  function handleModalClose(): void {
    if (onClose !== undefined) {
      onClose();
    }
  }

  return (
    <React.StrictMode>
      <Modal
        backdrop={true}
        bsSize={bsSize}
        dialogClassName={style.dialog}
        onHide={handleModalClose}
        show={open}
      >
        <Modal.Header className={style.header}>
          <Modal.Title className={style.title}>{headerTitle}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {content}
          {children}
        </Modal.Body>
        <Modal.Footer>{footer}</Modal.Footer>
      </Modal>
    </React.StrictMode>
  );
};

export { modal as Modal };
