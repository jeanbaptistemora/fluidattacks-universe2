/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { Container } from "../../../../components/Container";
import { Text } from "../../../../components/Typography";
import type { ITextProps } from "../../../../components/Typography";

const FaqBody: React.FC<ITextProps> = ({ children }): JSX.Element => (
  <Container mb={4}>
    <Text color={"#11111"} textAlign={"start"}>
      {children}
    </Text>
  </Container>
);

export { FaqBody };
