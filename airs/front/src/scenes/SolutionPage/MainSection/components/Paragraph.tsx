/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { Text } from "../../../../components/Typography";
import type { ITextProps } from "../../../../components/Typography";

const Paragraph: React.FC<ITextProps> = ({ children }): JSX.Element => (
  <Text color={"#535365"} mb={3} mt={3} size={"medium"}>
    {children}
  </Text>
);

export { Paragraph };
