import styled from "styled-components";

interface IContainerProps {
  width?: string;
}

const Container = styled.aside.attrs({
  className: "absolute overflow-x-hidden z-999",
})<IContainerProps>`
  ${({ width = "350px" }): string => `
  background-color: #f4f4f6;
  border-radius: 4px;
  border: solid 1px #d2d2da;
  bottom: 0;
  font-family: "Roboto", sans-serif;
  font-size: 16px;
  padding: 24px;
  right: 0;
  top: 0;
  width: ${width};
`}
`;
export { Container };
