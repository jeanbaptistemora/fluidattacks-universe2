import dayjs from "dayjs";

function isWithInAWeek(date: dayjs.Dayjs): boolean {
  const numberOfDays: number = 7;
  const weekOld: dayjs.Dayjs = dayjs()
    .subtract(numberOfDays, "days")
    .startOf("day");

  return date.isAfter(weekOld);
}

const formatIsoDate = (value: string): string =>
  dayjs(value).format("YYYY-MM-DD hh:mm:ss");

const getDatePlusDeltaDays = (date: string, days: number): string =>
  dayjs(date).add(days, "days").format("YYYY-MM-DD hh:mm:ss");

const getRemainingDays = (value: string): number =>
  dayjs(value).diff(dayjs(), "days");

export { formatIsoDate, getDatePlusDeltaDays, getRemainingDays, isWithInAWeek };
