// tslint:disable: no-console
import open from "open";
import webpack from "webpack";
import WebpackDevServer from "webpack-dev-server";
import devConfig from "./webpack.dev.config";

const HOST: string = "localhost";
const PORT: number = 3000;

process.on("unhandledRejection", (err: {} | null | undefined) => {
  throw err;
});

const compiler: webpack.Compiler = webpack(devConfig);
const serverConfig: WebpackDevServer.Configuration = {
  compress: true,
  headers: { "Access-Control-Allow-Origin": "*" },
  historyApiFallback: true,
  hot: true,
  https: true,
  publicPath: (devConfig.output as webpack.Output).publicPath,
  sockHost: HOST,
  sockPort: PORT,
  stats: devConfig.stats,
};

const devServer: WebpackDevServer = new WebpackDevServer(compiler, serverConfig);
devServer.listen(PORT, HOST, (err?: Error): void => {
  if (err !== undefined) {
    console.log(err);
  }

  console.log("Starting the development server...\n");
  open(`https://${HOST}:8080/integrates`)
    .catch();
});

(["SIGINT", "SIGTERM"] as NodeJS.Signals[]).forEach((sig: NodeJS.Signals): void => {
  process.on(sig, (): void => {
    devServer.close();
    process.exit();
  });
});
