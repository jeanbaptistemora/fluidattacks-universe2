import TerserPlugin from "terser-webpack-plugin";
import webpack from "webpack";

import { commonConfig } from "./webpack.common.config";

const prodConfig: webpack.Configuration = {
  ...commonConfig,
  bail: true,
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
    splitChunks: {
        chunks: "all",
      },
  },
};

export = prodConfig;
