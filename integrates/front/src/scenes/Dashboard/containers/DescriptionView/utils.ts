import _ from "lodash";

import { translate } from "utils/translations/translate";

const formatFindingType: (type: string) => string = (type: string): string =>
  _.isEmpty(type)
    ? "-"
    : translate.t(`searchFindings.tabDescription.type.${type.toLowerCase()}`);

const formatCompromisedRecords: (records: number) => string = (
  records: number
): string => records.toString();

export { formatFindingType, formatCompromisedRecords };
