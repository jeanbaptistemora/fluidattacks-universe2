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
