import React from "react";
import { Modal } from "react-bootstrap";
import style from "./index.css";

interface IModalProps {
  children?: React.ReactNode;
  content?: React.ReactNode;
  footer: React.ReactNode;
  headerTitle: string;
  open: boolean;
  onClose?(): void;
}

const modal: React.SFC<IModalProps> = (props: IModalProps): JSX.Element => {
  const handleModalClose: (() => void) = (): void => {
    if (props.onClose !== undefined) { props.onClose(); }
  };

  return (
    <React.StrictMode>
      <Modal show={props.open} onHide={handleModalClose} dialogClassName={style.dialog}>
        <Modal.Header className={style.header}>
          <Modal.Title className={style.title}>{props.headerTitle}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {props.content}{props.children}
        </Modal.Body>
        <Modal.Footer>
          {props.footer}
        </Modal.Footer>
      </Modal>
    </React.StrictMode>
  );
};

export = modal;
