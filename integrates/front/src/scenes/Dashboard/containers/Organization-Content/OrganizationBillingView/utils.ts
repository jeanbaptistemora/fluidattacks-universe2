import _ from "lodash";

const now: Date = new Date();
const thisYear: number = now.getFullYear();
const thisMonth: number = now.getMonth();
const DATE_RANGE = 12;
const dateRange: Date[] = _.range(0, DATE_RANGE).map(
  (month: number): Date => new Date(thisYear, thisMonth - month)
);

const formatDate: (date: Date) => string = (date: Date): string => {
  const month: number = date.getMonth() + 1;
  const monthStr: string = month.toString();

  return `${monthStr.padStart(2, "0")}/${date.getFullYear()}`;
};

export { dateRange, formatDate };
