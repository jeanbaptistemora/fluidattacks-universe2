/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const Field = styled.p.attrs({ className: "ma0 pv1" })``;

const Label = styled.span`
  :after {
    content: ": ";
  }
`;

export { Field, Label };
