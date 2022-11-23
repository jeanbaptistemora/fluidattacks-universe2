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
    poppins
    ma0
    mt3
    center
    mw-1038
  `,
})`
  line-height: 2rem;
`;

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
    poppins
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
    f5
    f4-ns
    c-gray-154
    poppins
    lh-15
    mt3
    mb5
    h-cycle-paragraph
  `,
})`
  max-width: 630px;
`;

const CycleControl = styled.button.attrs({
  className: "mt2 mr2 bn pointer",
})<{ active: boolean }>`
  background-color: ${({ active }): string => (active ? "#ff3435" : "#5c5c70")};
  height: 16px;
  width: 16px;
`;

const ProgressContainer = styled.div.attrs({
  className: `
    mb1
    relative
    br3
    center-m
    bg-black-gray
  `,
})`
  height: 10px;
  max-width: 315px;
`;

const ProgressBar = styled.div.attrs({
  className: `
    relative
    br3
    bg-gray-244
  `,
})<{ width: string }>`
  height: 100%;
  width: ${({ width }): string => width};
  transition: width 0.25s;
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
  ProgressBar,
  ProgressContainer,
  ServiceParagraph,
};
