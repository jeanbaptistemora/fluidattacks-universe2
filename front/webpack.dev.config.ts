import webpack from "webpack";

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
              publicPath: "https://localhost:3000/dashboard/img/",
            },
          },
        ],
      },
    ],
  },
  output: {
    ...commonConfig.output,
    publicPath: "https://localhost:3000/dashboard/",
  },
  plugins: [
    ...commonConfig.plugins as [],
    new webpack.HotModuleReplacementPlugin(),
  ],
};

export = devConfig;
