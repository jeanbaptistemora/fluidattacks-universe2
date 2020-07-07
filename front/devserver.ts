/* eslint-disable no-console
  --------
  We need console methods for easy debugging during development.
*/
import WebpackDevServer from "webpack-dev-server";
import devConfig from "./webpack.dev.config";
import open from "open";
import webpack from "webpack";

const HOST: string = "localhost";
const PORT: number = 3000;

process.on(
  "unhandledRejection",
  (reason: Error | unknown, promise: Readonly<Promise<unknown>>): void => {
    console.error("Unhandled Rejection at:", promise, "reason:", reason);
  }
);

const compiler: webpack.Compiler = webpack(devConfig);
const serverConfig: WebpackDevServer.Configuration = {
  compress: true,
  /*
   * Access-Control-Allow-Origin response header tell the browser that the
   * content on this page is accessible from all origins.
   */
  // eslint-disable-next-line @typescript-eslint/naming-convention
  headers: { "Access-Control-Allow-Origin": "*" },
  historyApiFallback: true,
  hot: true,
  https: true,
  publicPath: (devConfig.output as webpack.Output).publicPath,
  sockHost: HOST,
  sockPort: PORT,
  stats: devConfig.stats,
};

const devServer: WebpackDevServer = new WebpackDevServer(
  compiler,
  serverConfig
);
devServer.listen(PORT, HOST, (serverError?: Error): void => {
  if (serverError !== undefined) {
    console.log(serverError);
  }

  console.log("Starting the development server...\n");
  open(`https://${HOST}:8080/integrates`).catch((error?: Error): void => {
    console.error(error);
  });
});

(["SIGINT", "SIGTERM"] as NodeJS.Signals[]).forEach(
  (sig: NodeJS.Signals): void => {
    process.on(sig, (): void => {
      devServer.close();
      process.exit();
    });
  }
);
