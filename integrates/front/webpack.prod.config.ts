import OptimizeCssAssetsPlugin from "optimize-css-assets-webpack-plugin";
import TerserPlugin from "terser-webpack-plugin";
import { commonConfig } from "./webpack.common.config";
import type webpack from "webpack";

const branchName: string =
  process.env.CI_COMMIT_REF_NAME === undefined
    ? "master"
    : process.env.CI_COMMIT_REF_NAME;
const bucketName: string =
  branchName === "master"
    ? "integrates.front.production.fluidattacks.com"
    : "integrates.front.development.fluidattacks.com";

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
              publicPath: `https://${bucketName}/${branchName}/static/dashboard/img/`,
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
