/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    pv5
    ph-body
  `,
})`
  background-color: #f4f4f6;
`;

const PortraitContainer = styled.div.attrs({
  className: `
    flex
    center
    mw-1366
    flex-wrap
    justify-center
  `,
})``;

const CardContainer = styled.div.attrs({
  className: `
    tc
    pv5
    ph4
    br2
    w-100
  `,
})`
  background-color: #ffffff;
  box-shadow: 0px 0px 6px 3px rgba(0, 0, 0, 0.06);
`;

const ImageContainer = styled.div`
  max-width: 682px;
  max-height: 361px;
`;

export { CardContainer, Container, ImageContainer, PortraitContainer };
