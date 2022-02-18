import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    bg-black-18
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

const GridCardsContainer = styled.div.attrs({
  className: `
    cardgrid
    center
    flex-l
    flex-wrap
    justify-around
    mw-1920
    dn
  `,
})``;

const CarrouselCardsContainer = styled.div.attrs({
  className: `
    cardgrid
    db
    center
    mw-1920
    dn-l
  `,
})``;

const CardContainer = styled.div.attrs({
  className: `
    bg-transparent
    dib
    mh4-l
    center
    mt5
    tc
  `,
})`
  min-height: 15rem;
  width: 20rem;
`;

const CardTitle = styled.p.attrs({
  className: `
    white
    roboto
    f1
    mb1
    fw7
    mt0
  `,
})``;

const CardText = styled.p.attrs({
  className: `
    b
    mt0
    f5
    roboto
  `,
})<{ gray: boolean }>`
  color: ${({ gray }): string => (gray ? "#a5a5b6" : "#f4f4f6")};
`;

const ProgressContainer = styled.div.attrs({
  className: `
    tc
    mb5
    w-100
  `,
})`
  progress[value] {
    -webkit-appearance: none;
    appearance: none;
  }

  progress[value]::-webkit-progress-bar {
    height: 10px;
    border-radius: 20px;
    background-color: #5c5c70;
  }

  progress[value]::-webkit-progress-value {
    height: 10px;
    border-radius: 20px;
    background-color: #ff3435;
  }
`;

export {
  CardContainer,
  CardText,
  CardTitle,
  CarrouselCardsContainer,
  Container,
  GridCardsContainer,
  ProgressContainer,
  TitleContainer,
};
