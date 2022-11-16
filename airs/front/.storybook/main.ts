/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
/* eslint-disable react/forbid-component-props */
import { StorybookConfig } from "@storybook/core-common";

const config: StorybookConfig = {
  stories: ["../src/**/*.stories.mdx", "../src/**/*.stories.@(js|jsx|ts|tsx)"],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
  ],
  framework: "@storybook/react",
  core: {
    builder: "@storybook/builder-webpack5",
  },
  webpackFinal: (config) => {
    if (typeof config.module?.rules?.[0] === "object") {
      // Transpile Gatsby module because Gatsby includes un-transpiled ES6 code.
      config.module.rules[0].exclude = [
        /node_modules\/(?!(gatsby|gatsby-script)\/)/,
      ];

      if (
        Array.isArray(config.module.rules[0].use) &&
        typeof config.module.rules[0].use[0] === "object" &&
        typeof config.module.rules[0].use[0].options === "object"
      ) {
        // use babel-plugin-remove-graphql-queries to remove static queries from components when rendering in storybook
        config.module.rules[0].use[0].options.plugins.push([
          require.resolve("babel-plugin-remove-graphql-queries"),
          {
            stage:
              config.mode === `development` ? "develop-html" : "build-html",
            staticQueryDir: "page-data/sq/d",
          },
        ]);
      }
    }

    return config;
  },
};

export = config;
