import type { Moment } from "moment";
import moment from "moment";

function isWithInAWeek(date: Moment): boolean {
  const numberOfDays: number = 7;
  const weekOld: Moment = moment()
    .subtract(numberOfDays, "days")
    .startOf("day");

  return date.isAfter(weekOld);
}

export { isWithInAWeek };
