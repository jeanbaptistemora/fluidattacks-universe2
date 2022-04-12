import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    white
    center
    flex
    ph-body
  `,
})``;

const PlansContainer = styled.div.attrs({
  className: `
    center
    mv5
    w-100
  `,
})`
  max-width: 1500px;

  @media (max-width: 960px) {
    max-width: 800px;
  }
`;

const PlansTitle = styled.p.attrs({
  className: `
    f2
    c-fluid-bk
    fw6
    neue
    lh-solid
    ma0
    tc
  `,
})``;

const CardsContainer = styled.div.attrs({
  className: `
    flex
    mt5
    justify-center
  `,
})`
  flex-wrap: nowrap;

  @media (max-width: 960px) {
    flex-wrap: wrap;
  }
`;

const PlansParagraph = styled.p.attrs({
  className: `
    f5
    c-black-gray
    roboto
    ma0
    mt3
    tc
  `,
})``;

export {
  CardsContainer,
  Container,
  PlansContainer,
  PlansParagraph,
  PlansTitle,
};
