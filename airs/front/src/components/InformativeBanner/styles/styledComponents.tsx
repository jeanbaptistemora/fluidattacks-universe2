/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const BannerList = styled.ul.attrs({
  className: `
    list
    ma0
    pa0
    overflow-hidden
    flex
    flex-nowrap
  `,
})``;

const InformativeBannerContainer = styled.div.attrs({
  className: `
    cssmenu
    lh-solid
    cover
    w-100
    top-0
    t-all-linear-3
  `,
})<{ bgColor: string; isClose: boolean }>`
  background-color: ${({ bgColor }): string => bgColor};
  display: ${({ isClose }): string => (isClose ? "none" : "block")};
  position: sticky;
  z-index: 1;
`;

const BannerItem = styled.li.attrs({
  className: `
    mr3
    pr2
    pv1
    flex
    flex-wrap
  `,
})``;

const CloseContainer = styled.li.attrs({
  className: `
    mr3
    pr2
    pv1
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
    mv1
  `,
})`
  border-color: #f4f4f6;
`;

const BannerTitle = styled.p.attrs({
  className: `
    white
    fw7
    roboto
    lh-solid
    f3
    mv3-l
    mv2
  `,
})``;

const BannerSubtitle = styled.p.attrs({
  className: `
    white
    fw4
    roboto
    lh-solid
    f3
    mv3-l
    mv2
  `,
})``;

export {
  BannerButton,
  BannerItem,
  BannerList,
  BannerSubtitle,
  BannerTitle,
  CloseContainer,
  InformativeBannerContainer,
};
