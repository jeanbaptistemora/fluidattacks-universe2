/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";
import React from "react";

import type { IStatus } from ".";
import { Tag } from "components/Tag";
import { getBgColor } from "utils/colors";

const CompleteStatus: React.FC<IStatus> = ({
  status,
}: IStatus): JSX.Element => {
  if (status === "-") return <div />;

  const formatedStatus: string = _.capitalize(status).replace("_", " ");
  const currentStateBgColor = getBgColor(_.capitalize(status));

  return <Tag variant={currentStateBgColor}>{formatedStatus}</Tag>;
};

export { CompleteStatus };