import path from "path";
import webpack from "webpack";

export const commonConfig: webpack.Configuration = {
  entry: {
    contentHome: "./static/js/contentHome.ts",
    dynClasses: "./static/js/dynClasses.ts",
  },
  module: {
    rules: [
      {
        use: [
          {
            loader: "ts-loader",
            options: {
              configFile: "tsconfig.webpack.json",
              transpileOnly: true,
            },
          },
        ],
      },
    ],
  },
  output: {
    filename: "[name].min.js",
    futureEmitAssets: true,
    path: path.resolve(__dirname, "./static/js/tmp/"),
  },
  resolve: {
    extensions: [".js", ".ts"],
  },
  stats: {
    children: false,
    colors: true,
    modules: false,
  },
};
