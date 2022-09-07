/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { Moment } from "moment";
import moment from "moment";

function isWithInAWeek(date: Moment): boolean {
  const numberOfDays: number = 7;
  const weekOld: Moment = moment()
    .subtract(numberOfDays, "days")
    .startOf("day");

  return date.isAfter(weekOld);
}

const formatIsoDate = (value: string): string =>
  moment(value).format("YYYY-MM-DD hh:mm:ss");

export { formatIsoDate, isWithInAWeek };
