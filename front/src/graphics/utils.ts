import _ from "lodash";

export const defaultIfUndefined: <T extends unknown>(value: T | undefined | null, defaultValue: T) => T =
  <T extends unknown>(value: T | undefined | null, defaultValue: T): T =>
    _.isNull(value) || _.isUndefined(value) ? defaultValue : value;
