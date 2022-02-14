import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    bg-black-18
    center
    flex
    flex-wrap
  `,
})``;

const MainTextContainer = styled.div.attrs({
  className: `
    tc
    w-100
    center
    mt5
    ph-body
  `,
})``;

const ServiceParagraph = styled.p.attrs({
  className: `
    f3
    c-gray-154
    roboto
    lh-solid
    ma0
    mt3
    center
    mw-1038
  `,
})``;

const CycleContainer = styled.div.attrs({
  className: `
    w-100
    mb5
    cf
  `,
})``;

const CycleImageContainer = styled.div.attrs({
  className: `
    fl-l
    w-100
    w-50-l
    pt0-ns
    tc
  `,
})``;

const CycleTextContainer = styled.div.attrs({
  className: `
    fr-l
    w-100
    w-50-l
    center
    tl
    mt6-l
    mt4
    pl5
    pr5
  `,
})``;

const CycleTitle = styled.p.attrs({
  className: `
    f3
    white
    fw6
    neue
    lh-solid
    ma0
  `,
})`
  @media (max-width: 475px) {
    min-height: 48px;
  }

  @media (max-width: 350px) {
    min-height: 72px;
  }
`;

const CycleParagraph = styled.p.attrs({
  className: `
    f4
    c-gray-154
    roboto
    lh-solid
    mt3
    h-cycle-paragraph
  `,
})`
  max-width: 630px;
  min-height: 100px;

  @media (max-width: 1274px) {
    min-height: 140px;
  }

  @media (max-width: 1018px) {
    min-height: 160px;
  }

  @media (max-width: 950px) {
    min-height: 120px;
  }

  @media (max-width: 526px) {
    min-height: 140px;
  }

  @media (max-width: 509px) {
    min-height: 160px;
  }

  @media (max-width: 452px) {
    min-height: 180px;
  }

  @media (max-width: 411px) {
    min-height: 200px;
  }

  @media (max-width: 403px) {
    min-height: 220px;
  }

  @media (max-width: 371px) {
    min-height: 240px;
  }

  @media (max-width: 365px) {
    min-height: 270px;
  }
`;

const CycleControl = styled.button.attrs({
  className: "mt2 mr2 bn pointer",
})<{ active: boolean }>`
  background-color: ${({ active }): string => (active ? "#ff3435" : "#5c5c70")};
  height: 16px;
  width: 16px;
`;

export {
  Container,
  CycleContainer,
  CycleControl,
  CycleParagraph,
  CycleTextContainer,
  CycleTitle,
  CycleImageContainer,
  MainTextContainer,
  ServiceParagraph,
};
