import MiniCssExtractPlugin from "mini-css-extract-plugin";
import path from "path";
import webpack from "webpack";

export const commonConfig: webpack.Configuration = {
  entry: {
    app: "./src/app.tsx",
    login: "./src/scenes/Login/index.tsx",
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
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
      {
        include: /node_modules/,
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          "css-loader",
        ],
      },
      {
        exclude: /node_modules/,
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: "css-loader",
            options: {
              modules: true,
            },
          },
        ],
      },
    ],
  },
  output: {
    filename: "[name]-bundle.min.js",
    futureEmitAssets: true,
    path: path.resolve(__dirname, "../app/assets/dashboard/"),
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name]-style.min.css",
    }),
  ],
  resolve: {
    extensions: [".js", ".jsx", ".ts", ".tsx"],
  },
  stats: {
    children: false,
    colors: true,
    modules: false,
  },
};
