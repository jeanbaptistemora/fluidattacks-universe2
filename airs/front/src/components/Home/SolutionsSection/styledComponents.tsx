import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    bg-darker-blue
    center
    flex
    flex-wrap
  `,
})``;

const TitleContainer = styled.div.attrs({
  className: `
    w-100
    tc
    mt5
    ph-body
  `,
})``;

const CardContainer = styled.div.attrs({
  className: `
    br4
    ma3
    ma-auto
    bg-white
  `,
})`
  min-width: 350px;
`;

const CardTextContainer = styled.div.attrs({
  className: `
    pl4
    mh1
    mt3
  `,
})``;

const CardTitle = styled.h1.attrs({
  className: `
    c-fluid-bk
    f3
    b
    lh-solid
    mt2
    roboto
    mb2
  `,
})``;

const CardDescription = styled.p.attrs({
  className: `
    c-black-gray
    pr4
    fw3
    f5
    mt1
    roboto
  `,
})`
  min-height: 120px;
`;

const CardsContainer = styled.div.attrs({
  className: `
    relative
    center
    overflow-hidden
    mb5
  `,
})`
  width: 1528px;

  @media (max-width: 1527px) {
    width: 1146px;
  }

  @media (max-width: 1145px) {
    width: 764px;
  }

  @media (max-width: 763px) {
    width: 382px;
  }
`;

const ArrowContainer = styled.div.attrs({
  className: `
    mr2
    mv4
    tr
  `,
})``;

const ArrowButton = styled.button.attrs({
  className: `
    bg-black-18
    bn
    br2
    pa3
    dib
    mr2
    pointer
    outline-transparent
  `,
})<{ limit: boolean }>`
  opacity: ${({ limit }): string => (limit ? "50%" : "100%")};
`;

const IconContainerSmall = styled.div.attrs({
  className: `
    dib
    fr
    ml1
    mr3
  `,
})`
  width: 0.7rem;
`;

const SlideShow = styled.div.attrs({
  className: `
    flex
    overflow-hidden-l
    overflow-x-auto
    scroll-smooth
    center
  `,
})`
  width: 1528px;

  @media (max-width: 1527px) {
    width: 1146px;
  }

  @media (max-width: 1145px) {
    width: 764px;
  }

  @media (max-width: 763px) {
    width: 382px;
  }
`;

export {
  ArrowButton,
  ArrowContainer,
  Container,
  CardContainer,
  CardDescription,
  CardsContainer,
  CardTextContainer,
  CardTitle,
  IconContainerSmall,
  SlideShow,
  TitleContainer,
};
