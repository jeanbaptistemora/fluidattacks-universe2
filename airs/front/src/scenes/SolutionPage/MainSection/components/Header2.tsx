/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { Title } from "../../../../components/Typography";
import type { ITitleProps } from "../../../../components/Typography";

const Header2: React.FC<ITitleProps> = ({ children }): JSX.Element => (
  <Title color={"#2e2e38"} level={2} textAlign={"center"}>
    {children}
  </Title>
);

export { Header2 };
