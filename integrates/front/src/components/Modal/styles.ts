import styled from "styled-components";

const Container = styled.div.attrs({
  className: "absolute--fill fixed overflow-auto z-999",
})`
  align-items: center;
  background-color: #0008;
  display: flex;
  justify-content: center;
`;

const Dialog = styled.div`
  background-color: #f4f4f6;
  border-radius: 4px;
  color: #2e2e38;
  display: flex;
  flex-direction: column;
  font-family: "Roboto", sans-serif;
  font-size: 16px;
  max-height: 90%;
  max-width: 90%;
  padding: 24px;
`;

const Header = styled.div.attrs({
  className: "flex items-center justify-between mb3",
})``;

const Title = styled.p.attrs({
  className: "b f3 ma0",
})``;

export { Container, Dialog, Header, Title };
