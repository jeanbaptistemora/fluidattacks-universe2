import styled from "styled-components";

const CardContainer = styled.div.attrs({
  className: `
    mh3
    mb4
    pv4
    ph3
    tc
    br4
    w-100
  `,
})<{ isMachine: boolean }>`
  margin-top: ${({ isMachine }): string => (isMachine ? "0" : "47px")};
  background-color: ${({ isMachine }): string =>
    isMachine ? "#ffffff" : "#f4f4f6"};
  border-top-left-radius: ${({ isMachine }): string =>
    isMachine ? "unset !important" : "1rem"};
  border-top-right-radius: ${({ isMachine }): string =>
    isMachine ? "unset !important" : "1rem"};
  box-shadow: 0px 0px 6px 3px rgba(0, 0, 0, 0.06);
`;

const CardTitleContainer = styled.div.attrs({
  className: `
    mb4
    justify-center
  `,
})<{ isOpen: boolean }>`
  @media (max-width: 960px) {
    margin-bottom: ${({ isOpen }): string =>
      isOpen ? "2rem" : "0"} !important;
  }
`;

const OpenButton = styled.button.attrs({
  className: `
    f2
    bn
    fr
    pointer
    c-black-gray
    bg-transparent
    dn
  `,
})`
  @media (max-width: 960px) {
    display: block !important;
  }
`;

const CardTitle = styled.p.attrs({
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

const CardParagraph = styled.p.attrs({
  className: `
    f3
    pb4
    mb3
    c-black-gray
    roboto
    ma0
  `,
})<{ isOpen: boolean }>`
  border-bottom: solid 1px #ceced7;

  @media only screen and (min-width: 1016px) and (max-width: 1332px) {
    min-height: 141px;
  }

  @media only screen and (min-width: 961px) and (max-width: 1015px) {
    min-height: 177px;
  }

  @media (max-width: 960px) {
    display: ${({ isOpen }): string => (isOpen ? "block" : "none")};
  }
`;

const CardItemsContainer = styled.div.attrs({
  className: `
    center
  `,
})<{ isOpen: boolean }>`
  max-width: 600px;

  @media (max-width: 960px) {
    display: ${({ isOpen }): string => (isOpen ? "block" : "none")};
  }
`;

const CardItem = styled.div.attrs({
  className: `
    f3
    flex
    pb3
    mb3
    c-black-gray
    roboto
    ma0
    tl
  `,
})`
  border-bottom: solid 1px #ceced7;
`;

const MachineButton = styled.button.attrs({
  className: `
    outline-transparent
    bg-fluid-red
    bc-hovered-red
    hv-bg-fluid-dkred
    hv-bd-fluid-dkred
    pointer
    white
    f4
    dib
    t-all-3-eio
    bc-fluid-red
    ba
    roboto
    justify-center
    bw1
    w-100
    mh3
  `,
})`
  padding: 10px 16px;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
`;

export {
  CardContainer,
  CardItem,
  CardItemsContainer,
  CardParagraph,
  CardTitle,
  CardTitleContainer,
  MachineButton,
  OpenButton,
};
