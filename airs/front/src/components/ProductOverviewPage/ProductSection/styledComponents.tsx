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
    w-100
    flex-wrap-l
    overflow-x-auto
  `,
})``;

export { Container, SectionContainer };
