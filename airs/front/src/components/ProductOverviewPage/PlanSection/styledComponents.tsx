import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    bg-gray-233
    center
    flex
    flex-wrap
    ph-body
  `,
})``;

const ProductParagraph = styled.p.attrs({
  className: `
    c-black-gray
    roboto
    ma0
    mv4
    center
  `,
})<{ isSecundary: boolean }>`
  font-size: ${({ isSecundary }): string => (isSecundary ? "1rem" : "1.5rem")};
  line-height: 2rem;
  max-width: 1088px;
`;

const MainTextContainer = styled.div.attrs({
  className: `
    tc
    w-100
    center
    mt5
  `,
})``;

export { Container, MainTextContainer, ProductParagraph };
