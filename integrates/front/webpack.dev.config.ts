import type { Configuration } from "webpack";
import type { Configuration as DevServerConfig } from "webpack-dev-server";

import { commonConfig } from "./webpack.common.config";

interface IWebpackConfig extends Configuration {
  devServer: DevServerConfig;
}

const devConfig: IWebpackConfig = {
  ...commonConfig,
  devServer: {
    client: {
      overlay: true,
    },
    headers: { "Access-Control-Allow-Origin": "https://localhost:8001" },
    historyApiFallback: true,
    hot: true,
    port: 3000,
    server: "https",
  },
  devtool: false,
  mode: "development",
  output: {
    ...commonConfig.output,
    publicPath: "https://localhost:3000/dashboard/",
  },
};

export = devConfig;
