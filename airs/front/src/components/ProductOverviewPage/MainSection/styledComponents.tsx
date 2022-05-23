import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    center
    flex
    flex-wrap
    ph-body
  `,
})`
  background-color: #2e2e38;
`;

const ProductParagraph = styled.p.attrs({
  className: `
    roboto
    ma0
    mv4
    center
    f3
  `,
})`
  color: #f4f4f6;
  line-height: 2rem;
  max-width: 1088px;
`;

const MainTextContainer = styled.div.attrs({
  className: `
    tc
    w-100
    center
    mv5
  `,
})``;

export { Container, MainTextContainer, ProductParagraph };
