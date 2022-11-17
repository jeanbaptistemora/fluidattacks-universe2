/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const SlideContainer = styled.div.attrs({
  className: `
      center
    `,
})`
  width: 1440px;

  @media screen and (max-width: 1504px) {
    width: 1080px;
  }

  @media screen and (max-width: 1144px) {
    width: 720px;
  }

  @media screen and (max-width: 784px) {
    width: 360px;
  }
`;

export { SlideContainer };
