/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import CssMinimizerPlugin from "css-minimizer-webpack-plugin";
import TerserPlugin from "terser-webpack-plugin";
import type { Configuration } from "webpack";

import { CI_COMMIT_REF_NAME, INTEGRATES_BUCKET_NAME } from "./src/utils/ctx";
import { commonConfig } from "./webpack.common.config";

const prodConfig: Configuration = {
  ...commonConfig,
  bail: true,
  devtool: "source-map",
  mode: "production",
  optimization: {
    ...commonConfig.optimization,
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: true,
          output: {
            comments: false,
            ecma: 5,
          },
          parse: {
            ecma: 2019,
          },
        },
      }),
      new CssMinimizerPlugin(),
    ],
  },
  output: {
    ...commonConfig.output,
    publicPath: `https://${INTEGRATES_BUCKET_NAME}/${CI_COMMIT_REF_NAME}/static/dashboard/`,
  },
};

export = prodConfig;
