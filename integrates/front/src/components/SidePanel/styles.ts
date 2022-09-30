/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const Container = styled.aside.attrs({
  className: "absolute overflow-x-hidden z-999",
})`
  background-color: #f4f4f6;
  border-radius: 4px;
  border: solid 1px #d2d2da;
  bottom: 0;
  font-family: "Poppins", sans-serif;
  font-size: 16px;
  padding: 24px;
  right: 0;
  top: 0;
  width: 350px;
`;

export { Container };
