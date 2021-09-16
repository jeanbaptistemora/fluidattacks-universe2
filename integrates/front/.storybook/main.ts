import { StorybookConfig } from "@storybook/core-common";

const config: StorybookConfig = {
  core: { builder: "webpack5" },
  stories: ["../src/**/*.stories.mdx", "../src/**/*.stories.@(js|jsx|ts|tsx)"],
  addons: ["@storybook/addon-links", "@storybook/addon-essentials"],
};

export = config;
