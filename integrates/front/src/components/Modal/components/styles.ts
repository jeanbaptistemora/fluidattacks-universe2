import styled from "styled-components";

const ModalContainer = styled.div.attrs({
  className: "absolute--fill fixed overflow-auto z-999",
})`
  background-color: rgba(0, 0, 0, 0.4);
`;

const ModalDialog = styled.div`
  background-color: #f4f4f6;
  border: 1px solid #b0b0bf;
  margin: 10% auto;
  padding: 24px;
  width: 70%;
`;

const ModalHeader = styled.div.attrs<{ className: string }>({
  className: "pv3 ph2",
})``;

const ModalTitle = styled.h4.attrs({
  className: "color-inherit lh-solid ma0",
})``;

const ModalBody = styled.div.attrs({
  className: "relative pa4",
})``;

const ModalFooter = styled.div.attrs({
  className: "modalf-bt pa1-5 tr",
})``;

export {
  ModalBody,
  ModalContainer,
  ModalDialog,
  ModalFooter,
  ModalHeader,
  ModalTitle,
};
