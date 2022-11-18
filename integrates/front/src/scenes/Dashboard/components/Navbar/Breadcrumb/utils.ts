/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";

export const stylizeBreadcrumbItem: (item: string) => string = (
  item: string
): string => {
  if (/^F?\d{3}./u.exec(item)) {
    // In case of a finding title (i.e. "083. XML injection (XXE)")
    return item;
  }
  switch (item) {
    case "devsecops":
      return "DevSecOps";
    case "vulns":
      return "Vulnerabilities";
    case "outofscope":
      return "Out of the scope";
    default:
      return _.capitalize(item);
  }
};
