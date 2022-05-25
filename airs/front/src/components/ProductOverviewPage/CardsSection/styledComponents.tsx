import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    center
    flex
    flex-wrap
    ph-body
  `,
})`
  background: #f4f4f6;
`;

const CardContainer = styled.div.attrs({
  className: `
    bg-fluid-black
    mh3
    mb4
    pv4
    ph3
    tc
    br3
    w-100
  `,
})`
  max-width: 424px;
`;

const CardTitle = styled.p.attrs({
  className: `
    white
    roboto
    f3
    mb1
    fw7
    mv4
  `,
})``;

const CardText = styled.p.attrs({
  className: `
    c-fluid-gray
    b
    mt0
    f5
    roboto
  `,
})``;

const CardsContainer = styled.div.attrs({
  className: `
    center
    flex
    mb4
    mt5
    justify-around
    flex-wrap
    flex-nowrap-l
    mw-1920
  `,
})``;

const MainTextContainer = styled.div.attrs({
  className: `
    tc
    w-100
    center
    mt5
  `,
})``;

export {
  CardContainer,
  CardsContainer,
  CardText,
  CardTitle,
  Container,
  MainTextContainer,
};
