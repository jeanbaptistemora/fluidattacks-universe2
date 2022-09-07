/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";

import { translate } from "utils/translations/translate";

const formatFindingType: (type: string) => string = (type: string): string =>
  _.isEmpty(type)
    ? "-"
    : translate.t(`searchFindings.tabDescription.type.${type.toLowerCase()}`);

export { formatFindingType };
