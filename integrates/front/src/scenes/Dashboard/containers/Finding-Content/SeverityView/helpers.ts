import _ from "lodash";

import { translate } from "utils/translations/translate";

const tooltipPropHelper = (currentOption: string): string | undefined => {
  return _.isEmpty(currentOption)
    ? undefined
    : translate.t(currentOption.replace(/text/u, "tooltip"));
};

const mapSeveritytoStringValues = (
  values: Record<string, unknown>
): Record<string, string> => {
  return _.mapValues(values, function toString(value: unknown): string {
    return String(value);
  });
};

export { mapSeveritytoStringValues, tooltipPropHelper };
