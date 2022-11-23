import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    center
    flex
    flex-wrap
    ph-body
  `,
})`
  background-color: #dddde3;
`;

const CardContainer = styled.div.attrs({
  className: `
    tl
    mh3
    mb4
    pv5
    ph4
    br2
    w-100
  `,
})`
  max-width: 400px;
  background-color: #ffffff;
  box-shadow: 0px 0px 6px 3px rgba(0, 0, 0, 0.06);
`;

const CardDescription = styled.div.attrs({
  className: `
  `,
})`
  @media (min-width: 960px) {
    min-height: 120px;
  }
`;

const CardsContainer = styled.div.attrs({
  className: `
    center
    flex
    mb4
    mt5
    justify-center
    flex-wrap
    flex-nowrap-l
    w-100
  `,
})``;

const MainTextContainer = styled.div.attrs({
  className: `
    tc
    w-100
    center
    mt5
  `,
})`
  max-width: 1300px;
`;

export {
  CardContainer,
  CardDescription,
  CardsContainer,
  Container,
  MainTextContainer,
};
