import styled from "styled-components";

const Container = styled.div.attrs({
  className: "absolute--fill fixed overflow-auto z-999",
})`
  background-color: rgba(0, 0, 0, 0.4);
`;

const Dialog = styled.div`
  background-color: #f4f4f6;
  border: 1px solid #b0b0bf;
  font-family: "Roboto", sans-serif;
  font-size: 16px;
  margin: 10% auto;
  padding: 24px;
  width: 70%;
`;

export { Container, Dialog };
