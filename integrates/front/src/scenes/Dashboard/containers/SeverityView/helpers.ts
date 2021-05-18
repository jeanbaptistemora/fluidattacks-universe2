import _ from "lodash";

import { translate } from "utils/translations/translate";

const tooltipPropHelper = (currentOption: string): string | undefined => {
  return _.isEmpty(currentOption)
    ? undefined
    : translate.t(currentOption.replace(/text/u, "tooltip"));
};

export { tooltipPropHelper };
