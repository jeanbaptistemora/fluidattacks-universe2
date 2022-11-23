import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    flex
    center
    mw-1366
    flex-wrap
    justify-center
  `,
})``;

const CardContainer = styled.div.attrs({
  className: `
    tl
    w-50-l
    w-100
    ph4
    mv5
  `,
})`
  > img + p + p {
    min-height: 120px;
  }
`;

export { CardContainer, Container };
