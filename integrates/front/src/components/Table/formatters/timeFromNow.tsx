import moment from "moment";

export const timeFromNow: (value: string) => string = (
  value: string
): string => {
  const result: string = moment(value, "YYYY-MM-DD hh:mm:ss").fromNow();

  return result === "Invalid date" ? "-" : result;
};
