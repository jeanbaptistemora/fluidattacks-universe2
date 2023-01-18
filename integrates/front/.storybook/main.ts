import { StorybookConfig } from "@storybook/core-common";
import { commonConfig } from "../webpack.common.config";

const config: StorybookConfig = {
  core: { builder: "webpack5" },
  stories: ["../src/**/*.stories.mdx", "../src/**/*.stories.@(js|jsx|ts|tsx)"],
  addons: [
    "@storybook/addon-essentials",
    "@storybook/addon-a11y",
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

export default config;
