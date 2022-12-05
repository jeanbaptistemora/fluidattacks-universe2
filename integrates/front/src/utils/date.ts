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

const getDatePlusDeltaDays = (date: string, days: number): string =>
  moment(date).add(days, "days").format("YYYY-MM-DD hh:mm:ss");

const getRemainingDays = (value: string): number =>
  moment(value).diff(moment(), "days");

export { formatIsoDate, getDatePlusDeltaDays, getRemainingDays, isWithInAWeek };
