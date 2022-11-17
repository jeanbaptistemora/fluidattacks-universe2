/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { Container } from "../../../../components/Container";
import type { IContainerProps } from "../../../../components/Container/types";

const GridContainer: React.FC<IContainerProps> = ({
  children,
}): JSX.Element => (
  <Container
    center={true}
    direction={"row"}
    display={"flex"}
    justify={"start"}
    maxWidth={"1504px"}
    ph={4}
    wrap={"wrap"}
  >
    {children}
  </Container>
);

export { GridContainer };
