import { HotModuleReplacementPlugin } from "webpack";
import type webpack from "webpack";

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
    graphicsForGroup: [
      "webpack-dev-server/client?https://localhost:3000",
      "webpack/hot/only-dev-server",
      "./src/graphics/views/group.tsx",
    ],
    graphicsForOrganization: [
      "webpack-dev-server/client?https://localhost:3000",
      "webpack/hot/only-dev-server",
      "./src/graphics/views/organization.tsx",
    ],
    graphicsForPortfolio: [
      "webpack-dev-server/client?https://localhost:3000",
      "webpack/hot/only-dev-server",
      "./src/graphics/views/portfolio.tsx",
    ],
  },
  mode: "development",
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
  plugins: [...(commonConfig.plugins as []), new HotModuleReplacementPlugin()],
};

export = devConfig;
