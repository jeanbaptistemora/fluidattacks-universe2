import OptimizeCssAssetsPlugin from "optimize-css-assets-webpack-plugin";
import TerserPlugin from "terser-webpack-plugin";
import webpack from "webpack";
import { commonConfig } from "./webpack.common.config";

const bucketName: string = "fluidintegrates-static";
const branchName: string = process.env.CI_COMMIT_REF_NAME === undefined
  ? "master"
  : process.env.CI_COMMIT_REF_NAME;

const prodConfig: webpack.Configuration = {
  ...commonConfig,
  bail: true,
  mode: "production",
  module: {
    ...commonConfig.module,
    rules: [
      ...(commonConfig.module as webpack.Module).rules,
      {
        test: /\.(gif|jpg|png|svg)$/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "[hash].[ext]",
              outputPath: "img/",
              publicPath: `https://${bucketName}-${branchName}.s3.amazonaws.com/integrates/assets/dashboard/img/`,
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
