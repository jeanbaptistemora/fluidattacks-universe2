/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { Container } from "../../../../components/Container";
import { Title } from "../../../../components/Typography";
import type { ITitleProps } from "../../../../components/Typography";

const Header2: React.FC<ITitleProps> = ({ children }): JSX.Element => (
  <Container mb={3} ph={4} pt={5}>
    <Title color={"#2e2e38"} level={2} textAlign={"center"}>
      {children}
    </Title>
  </Container>
);

export { Header2 };
