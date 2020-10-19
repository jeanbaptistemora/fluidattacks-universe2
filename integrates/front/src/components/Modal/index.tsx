/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap
*/
import React from "react";
import style from "components/Modal/index.css";
import { Modal, Sizes } from "react-bootstrap";
import {
  ModalBody,
  ModalFooter,
  ModalHeader,
  ModalTitle,
} from "styles/styledComponents";

interface IModalProps {
  bsSize?: Sizes;
  children?: React.ReactNode;
  footer?: React.ReactNode;
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
    children,
    footer = <div />,
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
    <Modal
      backdrop={true}
      bsSize={bsSize}
      dialogClassName={style.dialog}
      onHide={handleModalClose}
      onShow={handleModalOpen}
      show={open}
    >
      <ModalHeader>
        <ModalTitle>{headerTitle}</ModalTitle>
      </ModalHeader>
      <ModalBody>{children}</ModalBody>
      <ModalFooter>{footer}</ModalFooter>
    </Modal>
  );
};

export { IModalProps, modal as Modal };
