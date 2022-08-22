import styled from "styled-components";

const Container = styled.aside.attrs({
  className: "absolute overflow-x-hidden z-999",
})`
  background-color: #f4f4f6;
  border-radius: 4px;
  border: solid 1px #d2d2da;
  bottom: 0;
  font-family: "Roboto", sans-serif;
  font-size: 16px;
  padding: 24px;
  right: 0;
  top: 0;
  width: 350px;
`;

export { Container };
