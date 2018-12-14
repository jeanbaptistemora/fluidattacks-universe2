/* tslint:disable:jsx-no-lambda
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 */
import React from "react";
import { Modal } from "react-bootstrap";
import style from "./index.css";

interface IModalProps {
  content: React.ReactNode;
  footer: React.ReactNode;
  headerTitle: string;
  open: boolean;
  onClose?(): void;
}

const modal: React.StatelessComponent<IModalProps> =
  (props: IModalProps): JSX.Element => (
    <React.StrictMode>
      <Modal show={props.open} onHide={(): void => { if (props.onClose !== undefined) { props.onClose(); } }}>
        <Modal.Header className={style.header}>
          <Modal.Title className={style.title}>{props.headerTitle}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {props.content}
        </Modal.Body>
        <Modal.Footer>
          {props.footer}
        </Modal.Footer>
      </Modal>
    </React.StrictMode>
  );

export = modal;
