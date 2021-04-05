import OptimizeCssAssetsPlugin from "optimize-css-assets-webpack-plugin";
import TerserPlugin from "terser-webpack-plugin";
import type webpack from "webpack";

import { CI_COMMIT_REF_NAME, INTEGRATES_BUCKET_NAME } from "./src/utils/ctx";
import { commonConfig } from "./webpack.common.config";

const prodConfig: webpack.Configuration = {
  ...commonConfig,
  bail: true,
  devtool: "source-map",
  mode: "production",
  module: {
    ...commonConfig.module,
    rules: [
      ...(commonConfig.module as webpack.Module).rules,
      {
        test: /\.(?<extension>gif|jpg|png|svg)$/u,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "[hash].[ext]",
              outputPath: "img/",
              publicPath: `https://${INTEGRATES_BUCKET_NAME}/${CI_COMMIT_REF_NAME}/static/dashboard/img/`,
            },
          },
        ],
      },
    ],
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        cache: true,
        terserOptions: {
          compress: true,
          output: {
            comments: false,
            ecma: 5,
          },
          parse: {
            ecma: 9,
          },
        },
      }),
      new OptimizeCssAssetsPlugin(),
    ],
  },
};

export = prodConfig;
