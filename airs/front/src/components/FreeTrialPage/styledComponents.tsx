import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    flex
    center
    flex-wrap
    justify-center
  `,
})`
  min-height: 100vh;
`;

const WhiteContainer = styled.div.attrs({
  className: `
    w-50-l
    w-100
    flex
    ph5
    items-center
    relative
  `,
})`
  background-color: #f4f4f6;
  > img {
    top: 50px;
  }
`;

const BlackContainer = styled.div.attrs({
  className: `
    w-50-l
    w-100
    flex
    ph5
    items-center
  `,
})`
  background-color: #1c1c22;
`;

const InternalContainer = styled.div.attrs({
  className: `
    mw-1366
    center
  `,
})``;

export { BlackContainer, Container, InternalContainer, WhiteContainer };
