/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";
import React from "react";

import { TableLink } from "components/Table/styles";

export function formatLinkHandler(link: string, text: string): JSX.Element {
  return <TableLink to={link}>{_.capitalize(text)}</TableLink>;
}
