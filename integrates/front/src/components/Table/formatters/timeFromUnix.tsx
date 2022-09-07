/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import moment from "moment";

export const timeFromUnix: (value: number) => string = (
  value: number
): string => {
  if (value < 0) {
    return "-";
  }

  const result: string = moment(value).format("YYYY-MM-DD hh:mm:ss");

  return result === "Invalid date" ? "-" : result;
};
