import styled from "styled-components";

const Container = styled.div.attrs({
  className: "word-wrap",
})``;

const QuestionButton = styled.button.attrs(
  ({ type }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: `outline-0 pa0`,
    type: type ?? "button",
  })
)`
  border: 0 !important;
  color: #ff3435;

  :hover {
    background-color: unset !important;
    color: #272727 !important;
  }
`;

export { Container, QuestionButton };
