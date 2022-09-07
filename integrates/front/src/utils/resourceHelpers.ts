/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";

export const openUrl: (url: string) => void = (url: string): void => {
  const newTab: Window | null = window.open(
    url,
    undefined,
    "noopener,noreferrer,"
  );
  if (_.isObject(newTab)) {
    // It is necessary to assign null to opener
    // eslint-disable-next-line fp/no-mutation
    newTab.opener = null;
  }
};
