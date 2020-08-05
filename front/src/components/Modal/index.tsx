/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap
*/
import React from "react";
import { default as style } from "./index.css";
import { Modal, Sizes } from "react-bootstrap";

export interface IModalProps {
  bsSize?: Sizes;
  children?: React.ReactNode;
  content?: React.ReactNode;
  footer: React.ReactNode;
  headerTitle: string;
  open: boolean;
  onClose?: () => void;
  onOpen?: () => void;
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
    onOpen,
  } = props;

  function handleModalClose(): void {
    if (onClose !== undefined) {
      onClose();
    }
  }

  function handleModalOpen(): void {
    if (onOpen !== undefined) {
      onOpen();
    }
  }

  return (
    <React.StrictMode>
      <Modal
        backdrop={true}
        bsSize={bsSize}
        dialogClassName={style.dialog}
        onHide={handleModalClose}
        onShow={handleModalOpen}
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
