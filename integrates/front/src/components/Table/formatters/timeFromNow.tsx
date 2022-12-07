import dayjs, { extend } from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import _ from "lodash";

export const timeFromNow: (value: string) => string = (
  value: string
): string => {
  const date = new Date(value);
  if (_.isEmpty(value) || isNaN(date.getTime())) return "-";

  extend(relativeTime);

  return dayjs(value, "YYYY-MM-DD hh:mm:ss").fromNow();
};
