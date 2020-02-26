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
  onClose?(): void;
}

const modal: React.FC<IModalProps> = (props: IModalProps): JSX.Element => {
  const handleModalClose: (() => void) = (): void => {
    if (props.onClose !== undefined) { props.onClose(); }
  };

  const bsSize: Sizes = props.bsSize === undefined ? "medium" : props.bsSize;

  return (
    <React.StrictMode>
      <Modal
        backdrop={true}
        bsSize={bsSize}
        dialogClassName={style.dialog}
        onHide={handleModalClose}
        show={props.open}
      >
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

export { modal as Modal };
