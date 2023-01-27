import dayjs from "dayjs";

import type { ISelectedOptions } from "../types";

function formatValue(
  value: string | undefined,
  mappedOptions: ISelectedOptions[] | undefined
): string | undefined {
  const formattedValue =
    mappedOptions === undefined
      ? value
      : mappedOptions.find((option): boolean => option.value === value)?.header;

  return formattedValue;
}

function formatCheckValues(
  checkValues: string[] | undefined,
  mappedOptions: ISelectedOptions[] | undefined
): string | undefined {
  const formattedCheckValues =
    checkValues === undefined
      ? undefined
      : checkValues
          .map(
            (checkValue): string =>
              mappedOptions?.find(
                (option): boolean => option.value === checkValue
              )?.header ?? ""
          )
          .join(", ");

  return formattedCheckValues;
}

function formatNumberRange(rangeValues: string[]): string | undefined {
  if (rangeValues[0] !== "" && rangeValues[1] !== "") {
    return `${rangeValues[0]} - ${rangeValues[1]}`;
  }
  if (rangeValues[0] !== "") {
    return `Min ${rangeValues[0]}`;
  }
  if (rangeValues[1] !== "") {
    return `Max ${rangeValues[1]}`;
  }

  return undefined;
}

function formatDateRange(rangeValues: string[]): string | undefined {
  if (rangeValues[0] !== "" && rangeValues[1] !== "") {
    return `${dayjs(rangeValues[0]).format("LL")} - ${dayjs(
      rangeValues[1]
    ).format("LL")}`;
  }
  if (rangeValues[0] !== "") {
    return `From ${dayjs(rangeValues[0]).format("LL")}`;
  }
  if (rangeValues[1] !== "") {
    return `To ${dayjs(rangeValues[1]).format("LL")}`;
  }

  return undefined;
}

export { formatCheckValues, formatDateRange, formatNumberRange, formatValue };
