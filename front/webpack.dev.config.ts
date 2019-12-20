import webpack from "webpack";
import { default as BundleTracker } from "webpack-bundle-tracker";

import { commonConfig } from "./webpack.common.config";

const devConfig: webpack.Configuration = {
  ...commonConfig,
  devtool: "cheap-module-source-map",
  entry: {
    app: [
      "webpack-dev-server/client?https://localhost:3000",
      "webpack/hot/only-dev-server",
      "./src/app.tsx",
    ],
    login: [
      "webpack-dev-server/client?https://localhost:3000",
      "webpack/hot/only-dev-server",
      "./src/scenes/Login/index.tsx",
    ],
  },
  mode: "development",
  output: {
    ...commonConfig.output,
    publicPath: "https://localhost:3000/dashboard/",
  },
  plugins: [
    ...commonConfig.plugins as [],
    new webpack.HotModuleReplacementPlugin(),
    new BundleTracker({
      filename: "webpack-stats.json",
      logTime: false,
      path: "../",
      publicPath: (commonConfig.output as webpack.Output).publicPath as string,
    }),
  ],
};

export = devConfig;
