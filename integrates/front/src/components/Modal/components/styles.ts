import styled from "styled-components";

const ModalContainer = styled.div.attrs({
  className: "absolute--fill fixed overflow-auto z-999",
})`
  background-color: rgba(0, 0, 0, 0.4);
`;

const ModalDialog = styled.div`
  background-color: #f4f4f6;
  border: 1px solid #b0b0bf;
  font-family: "Roboto", sans-serif;
  font-size: 16px;
  margin: 10% auto;
  padding: 24px;
  width: 70%;
`;

const ModalHeader = styled.div.attrs<{ className: string }>({
  className: "flex items-center justify-between mb3",
})``;

const ModalTitle = styled.p.attrs({
  className: "ma0 pa0",
})``;

const ModalBody = styled.div``;

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
