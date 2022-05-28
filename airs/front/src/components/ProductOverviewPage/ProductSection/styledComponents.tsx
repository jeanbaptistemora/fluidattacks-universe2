import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    center
    ph-body
    bg-white
  `,
})``;

const SectionContainer = styled.div.attrs({
  className: `
    center
    flex
    flex-wrap-l
    overflow-x-auto
  `,
})`
  @media (max-width: 960px) {
    width: 564px;
  }
  @media (max-width: 700px) {
    width: 364px;
  }

  @media (max-width: 500px) {
    width: 264px;
  }
`;

export { Container, SectionContainer };
