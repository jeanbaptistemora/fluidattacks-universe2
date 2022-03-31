import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    white
    center
    flex
    ph-body
  `,
})``;

const FaqContainer = styled.div.attrs({
  className: `
    center
    mv5
  `,
})`
  width: 1088px;
`;

const FaqParagraph = styled.p.attrs({
  className: `
    f3
    c-black-gray
    roboto
    ma0
    mt5
    tc
  `,
})`
  line-height: 2rem;

  a {
    color: #5c5c70;
  }
`;

export { Container, FaqContainer, FaqParagraph };
