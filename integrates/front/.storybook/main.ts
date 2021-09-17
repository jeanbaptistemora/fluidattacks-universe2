import { StorybookConfig } from "@storybook/core-common";
import { commonConfig } from "../webpack.common.config";

const config: StorybookConfig = {
  core: { builder: "webpack5" },
  stories: ["../src/**/*.stories.mdx", "../src/**/*.stories.@(js|jsx|ts|tsx)"],
  addons: ["@storybook/addon-links", "@storybook/addon-essentials"],
  webpackFinal: (config) => ({
    ...config,
    resolve: {
      ...config.resolve,
      ...commonConfig.resolve,
    },
  }),
};

export = config;
