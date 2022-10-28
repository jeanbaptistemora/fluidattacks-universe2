/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    db
  `,
})``;

const Col = styled.div.attrs({
  className: `
    tc
    mv3
    flex
  `,
})``;

const LineCol = styled.div.attrs({
  className: `
    absolute
  `,
})``;

const Line = styled.div.attrs({
  className: `
    relative
  `,
})`
  background-color: #b0b0bf;
  height: 55px;
  width: 3px;
  top: -35px;
  left: 6px;
`;

const TextContainer = styled.div.attrs({
  className: `
    db
    tl
  `,
})``;

const Text = styled.p.attrs({
  className: `
    poppins
    ma0
  `,
})`
  color: #5c5c70;
  font-size: 1rem !important;
  @media screen and (max-width: 365px) {
    font-size: 0.8rem !important;
  }
`;

export { Col, Container, Line, LineCol, Text, TextContainer };
