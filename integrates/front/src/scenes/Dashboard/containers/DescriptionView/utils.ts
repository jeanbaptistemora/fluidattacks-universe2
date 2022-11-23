import _ from "lodash";

import { translate } from "utils/translations/translate";

const formatFindingType: (type: string) => string = (type: string): string =>
  _.isEmpty(type)
    ? "-"
    : translate.t(`searchFindings.tabDescription.type.${type.toLowerCase()}`);

export { formatFindingType };
