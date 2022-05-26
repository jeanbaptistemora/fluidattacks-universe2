import styled from "styled-components";

const Container = styled.div.attrs({
  className: "word-wrap",
})``;

const LinkSpan = styled.span.attrs({})<{
  isNone: boolean;
}>`
  border: none;
  border-bottom: ${({ isNone }): string => (isNone ? "0" : "solid 1px")};
  color: #5c5c70;
  cursor: pointer;
  opacity: ${({ isNone }): string => (isNone ? "50%" : "100%")};

  :hover {
    color: #2e2e38;
  }
`;

export { Container, LinkSpan };
