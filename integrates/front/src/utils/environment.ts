/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";

type Environment = "development" | "ephemeral" | "production";

export const getEnvironment: () => Environment = (): Environment => {
  if (_.isUndefined(window)) {
    return "development";
  }
  const currentUrl: string = window.location.hostname;
  const ephemeralDomainRegex: RegExp = /[a-z]+atfluid.app.fluidattacks.com/gu;

  if (currentUrl === "localhost") {
    return "development";
  } else if (ephemeralDomainRegex.test(currentUrl)) {
    return "ephemeral";
  }

  return "production";
};
