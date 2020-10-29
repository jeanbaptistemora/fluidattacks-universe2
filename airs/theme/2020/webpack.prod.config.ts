import _ from "lodash";
import TerserPlugin from "terser-webpack-plugin";
import webpack from "webpack";
import {
  BugsnagBuildReporterPlugin,
  BugsnagSourceMapUploaderPlugin,
} from "webpack-bugsnag-plugins";

import { commonConfig } from "./webpack.common.config";

const appVersion: string = _.isString(process.env.CI_COMMIT_SHORT_SHA)
? process.env.CI_COMMIT_SHORT_SHA
: "";
const commitSha: string = _.isString(process.env.CI_COMMIT_SHA)
  ? process.env.CI_COMMIT_SHA
  : "";
let bugsnagApiKey: string; bugsnagApiKey = "6d0d7e66955855de59cfff659e6edf31";
const branchName: string =
  // tslint:disable-next-line: strict-comparisons
  process.env.CI_COMMIT_REF_NAME === undefined
    ? "master"
    : process.env.CI_COMMIT_REF_NAME;
let bucketName: string;

branchName === "master"
  ? bucketName = "fluidattacks.com"
  : bucketName = "web.eph.fluidattacks.com";

let sourceMapPath: string;

branchName === "master"
  ? sourceMapPath = `https://${bucketName}.s3.amazonaws.com/theme/js/tmp/`
  : sourceMapPath = `https://${bucketName}.s3.amazonaws.com/${branchName}/theme/js/tmp/`;

const prodConfig: webpack.Configuration = {
  ...commonConfig,
  bail: true,
  devtool: "source-map",
  mode: "production",
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
    ],
  },
  plugins: [
    new BugsnagSourceMapUploaderPlugin({
      apiKey: bugsnagApiKey,
      appVersion,
      overwrite: true,
      publicPath: sourceMapPath,
    }),
    new BugsnagBuildReporterPlugin({
      apiKey: bugsnagApiKey,
      appVersion,
      sourceControl: {
        provider: "gitlab",
        repository: "https://gitlab.com/fluidattacks/product.git",
        revision: `${commitSha}/product/airs`,
      },
    }),
  ],
};

export = prodConfig;
