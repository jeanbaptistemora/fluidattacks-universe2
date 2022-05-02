import styled from "styled-components";

const InformativeBannerContainer = styled.div.attrs({
  className: `
    cssmenu
    lh-solid
    cover
    w-100
    top-0
    z-max
    t-all-linear-3
  `,
})<{ bgColor: string; isClose: boolean }>`
  background-color: ${({ bgColor }): string => bgColor};
  display: ${({ isClose }): string => (isClose ? "none" : "block")};
`;

const BannerItem = styled.li.attrs({
  className: `
    mr3
    pr2
    pv3
    flex
    flex-wrap
  `,
})``;

const CloseContainer = styled.li.attrs({
  className: `
    mr3
    pr2
    pv3
    flex-l
    dn
  `,
})``;

const BannerButton = styled.button.attrs({
  className: `
    outline-transparent
    bg-fluid-red
    hv-bg-fluid-dkred
    pointer
    white
    pv3
    ph3
    fw7
    f5
    dib
    t-all-3-eio
    br2
    ba
    roboto
    mt2
  `,
})`
  border-color: #f4f4f6;
`;

const BannerTitle = styled.h2.attrs({
  className: `
    white
    fw7
    neue
    lh-solid
  `,
})``;

const BannerSubtitle = styled.h2.attrs({
  className: `
    white
    fw1
    neue
    lh-solid
  `,
})``;

export {
  BannerButton,
  BannerItem,
  BannerSubtitle,
  BannerTitle,
  CloseContainer,
  InformativeBannerContainer,
};
