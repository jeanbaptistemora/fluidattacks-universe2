/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

const getProgressBarColor: (progress: number) => string = (
  progress: number
): string => {
  const LOW_PROGRESS_LIMIT = 30;
  const MEDIUM_PROGRESS_LIMIT = 70;
  if (progress <= LOW_PROGRESS_LIMIT) {
    return "#009245";
  } else if (progress <= MEDIUM_PROGRESS_LIMIT) {
    return "#FF961E";
  }

  return "#BF0B1A";
};

export { getProgressBarColor };
