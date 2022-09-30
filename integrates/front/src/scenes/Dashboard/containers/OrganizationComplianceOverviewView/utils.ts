/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";

const handleComplianceValue: (value: number | null) => number = (
  value: number | null
  // eslint-disable-next-line @typescript-eslint/no-magic-numbers
): number => (_.isNull(value) ? 0 : value * 100);

const getProgressBarColor: (progress: number) => string = (
  progress: number
): string => {
  const LOW_PROGRESS_LIMIT = 30;
  const MEDIUM_PROGRESS_LIMIT = 70;
  if (progress <= LOW_PROGRESS_LIMIT) {
    return "#BF0B1A";
  } else if (progress <= MEDIUM_PROGRESS_LIMIT) {
    return "#FF961E";
  }

  return "#009245";
};

export { getProgressBarColor, handleComplianceValue };
