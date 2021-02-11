import moment from "moment";

export const dateFormatter: (value: string) => string = (
  value: string
): string => moment(value).format("YYYY-MM-DD hh:mm:ss");
