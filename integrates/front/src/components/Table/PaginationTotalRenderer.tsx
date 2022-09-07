/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { Text } from "components/Text";

const PaginationTotalRenderer = (
  from: number,
  to: number,
  size: number
): JSX.Element => (
  <Text bright={5} disp={"inline"} ml={3} size={2} tone={"light"}>
    {`${from} - ${to} of ${size}`}
  </Text>
);

export { PaginationTotalRenderer };
