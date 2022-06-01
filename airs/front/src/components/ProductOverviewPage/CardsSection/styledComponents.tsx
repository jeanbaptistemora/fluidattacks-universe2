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
    pv2
    ph4
    tc
    br2
    w-100
  `,
})`
  max-width: 300px;
  background-color: #ffffff;
  box-shadow: 0px 0px 6px 3px rgba(0, 0, 0, 0.06);
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
  CardsContainer,
  CardTitle,
  Container,
  MainTextContainer,
};
