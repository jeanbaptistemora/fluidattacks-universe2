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

const CardsContainer = styled.div.attrs({
  className: `
    cardgrid
    db
    center
    flex-l
    flex-wrap-l
    justify-around-l
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

export {
  CardContainer,
  CardText,
  CardTitle,
  CardsContainer,
  Container,
  TitleContainer,
};
