/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    flex
    center
    flex-wrap
    justify-center
  `,
})`
  min-height: 100vh;
`;

const WhiteContainer = styled.div.attrs({
  className: `
    w-50-l
    w-100
    flex
    flex-wrap
    ph-body
    items-center
    flex-column
    justify-center
  `,
})`
  background-color: #f4f4f6;
`;

const BlackContainer = styled.div.attrs({
  className: `
    w-50-l
    w-100
    flex
    ph-body
    items-center
  `,
})`
  background-color: #1c1c22;
`;

const InternalContainer = styled.div.attrs({
  className: `
    mw-1366
    center
    mv4
  `,
})`
  > ul {
    padding-left: 1rem;
  }
`;

const ImageContainer = styled.div.attrs({
  className: `
    mw-1366
    mt4
  `,
})``;

export {
  BlackContainer,
  Container,
  ImageContainer,
  InternalContainer,
  WhiteContainer,
};
