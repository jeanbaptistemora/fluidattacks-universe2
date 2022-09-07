/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import moment from "moment";

export const timeFromNow: (value: string) => string = (
  value: string
): string => {
  const result: string = moment(value, "YYYY-MM-DD hh:mm:ss").fromNow();

  return result === "Invalid date" ? "-" : result;
};
