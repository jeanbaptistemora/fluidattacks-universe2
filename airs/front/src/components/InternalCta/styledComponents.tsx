/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const BannerContainer = styled.div.attrs({
  className: `
    pv5
    flex
    center
    ph-body
    flex-wrap
    items-center
  `,
})`
  max-width: 1600px;
`;

const TextContainer = styled.div.attrs({
  className: `
    tl
    w-100
    ma0-l
    mb4
    w-50-l
  `,
})``;

const ImageContainer = styled.div.attrs({
  className: `
    w-50-l
    w-100
    center
    relative
  `,
})``;

export { BannerContainer, ImageContainer, TextContainer };
