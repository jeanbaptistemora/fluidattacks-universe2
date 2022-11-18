/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { Container } from "../../../../components/Container";
import type { IContainerProps } from "../../../../components/Container/types";

const FaqContainer: React.FC<IContainerProps> = ({ children }): JSX.Element => (
  <Container
    borderBottom={"2px"}
    center={true}
    maxWidth={"1200px"}
    mb={5}
    mt={5}
  >
    {children}
  </Container>
);

export { FaqContainer };
