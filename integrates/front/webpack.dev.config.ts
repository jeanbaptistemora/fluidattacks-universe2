import type { Configuration } from "webpack";
import { HotModuleReplacementPlugin } from "webpack";
import type { Configuration as DevServerConfig } from "webpack-dev-server";

import { commonConfig } from "./webpack.common.config";

interface IWebpackConfig extends Configuration {
  devServer: DevServerConfig;
}

const devConfig: IWebpackConfig = {
  ...commonConfig,
  devServer: {
    compress: true,
    headers: { "Access-Control-Allow-Origin": "https://localhost:8001" },
    historyApiFallback: true,
    hot: true,
    https: true,
    overlay: true,
    port: 3000,
    publicPath: (commonConfig.output as NonNullable<IWebpackConfig["output"]>)
      .publicPath as string,
  },
  devtool: false,
  mode: "development",
  output: {
    ...commonConfig.output,
    publicPath: "https://localhost:3000/dashboard/",
  },
  plugins: [...(commonConfig.plugins as []), new HotModuleReplacementPlugin()],
};

export = devConfig;
