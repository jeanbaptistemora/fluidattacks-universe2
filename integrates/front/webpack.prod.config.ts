import OptimizeCssAssetsPlugin from "optimize-css-assets-webpack-plugin";
import TerserPlugin from "terser-webpack-plugin";
import _ from "lodash";
import { commonConfig } from "./webpack.common.config";
import webpack from "webpack";
import {
  BugsnagBuildReporterPlugin,
  BugsnagSourceMapUploaderPlugin,
} from "webpack-bugsnag-plugins";

const appVersion: string = _.isString(process.env.FI_VERSION)
  ? process.env.FI_VERSION
  : "";
const commitSha: string = _.isString(process.env.CI_COMMIT_SHA)
  ? process.env.CI_COMMIT_SHA
  : "";
const bugsnagApiKey: string = "99a64555a50340cfa856f6623c6bf35d";
const bucketName: string = "fluidintegrates-static";
const branchName: string =
  process.env.CI_COMMIT_REF_NAME === undefined
    ? "master"
    : process.env.CI_COMMIT_REF_NAME;

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
        test: /\.(gif|jpg|png|svg)$/u,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "[hash].[ext]",
              outputPath: "img/",
              publicPath: `https://${bucketName}-${branchName}.s3.amazonaws.com/integrates/static/dashboard/img/`,
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
  plugins: [
    ...(commonConfig.plugins as []),
    new BugsnagSourceMapUploaderPlugin({
      apiKey: bugsnagApiKey,
      appVersion,
      publicPath: `https://${bucketName}-${branchName}.s3.amazonaws.com/integrates/static/dashboard/`,
    }),
    new BugsnagBuildReporterPlugin({
      apiKey: bugsnagApiKey,
      appVersion,
      sourceControl: {
        provider: "gitlab",
        repository: "https://gitlab.com/fluidattacks/product.git",
        revision: `${commitSha}/integrates/front`,
      },
    }),
  ],
};

export = prodConfig;
