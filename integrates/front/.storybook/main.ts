/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { StorybookConfig } from "@storybook/core-common";
import { commonConfig } from "../webpack.common.config";

const config: StorybookConfig = {
  core: { builder: "webpack5" },
  stories: ["../src/**/*.stories.mdx", "../src/**/*.stories.@(js|jsx|ts|tsx)"],
  addons: [
    "@storybook/addon-a11y",
    "@storybook/addon-essentials",
    "@storybook/addon-links",
  ],
  webpackFinal: (config) => ({
    ...config,
    resolve: {
      ...config.resolve,
      ...commonConfig.resolve,
    },
  }),
};

export = config;
