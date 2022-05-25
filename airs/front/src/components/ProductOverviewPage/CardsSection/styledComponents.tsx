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
    mh3
    mb4
    pv4
    ph4
    tc
    br2
    w-100
  `,
})`
  max-width: 400px;
  background-color: #ffffff;
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
})`
  max-width: 1300px;
`;

export {
  CardContainer,
  CardsContainer,
  CardTitle,
  Container,
  MainTextContainer,
};
