import path from "path";

import MiniCssExtractPlugin from "mini-css-extract-plugin";
import type { Configuration } from "webpack";

export const commonConfig: Configuration = {
  entry: {
    app: "./src/app.tsx",
    graphicsForGroup: "./src/graphics/views/group.tsx",
    graphicsForOrganization: "./src/graphics/views/organization.tsx",
    graphicsForPortfolio: "./src/graphics/views/portfolio.tsx",
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/u,
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
        include: /node_modules/u,
        test: /\.css$/u,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          "css-loader",
        ],
      },
      {
        exclude: /node_modules/u,
        test: /\.css$/u,
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
      {
        generator: {
          filename: "img/[hash][ext]",
        },
        test: /\.(?<extension>gif|jpg|png|svg)$/u,
        type: "asset/resource",
      },
      {
        test: /\.(?<ext>woff|woff2)/u,
        use: [{ loader: "file-loader" }],
      },
    ],
  },
  output: {
    clean: true,
    filename: "[name]-bundle.min.js",
    path: path.resolve(__dirname, "../app/static/dashboard/"),
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name]-style.min.css",
    }),
  ],
  resolve: {
    alias: {
      components: path.join(__dirname, "src", "components"),
      graphics: path.join(__dirname, "src", "graphics"),
      // https://github.com/react-bootstrap-table/react-bootstrap-table2/issues/1520
      "react-bootstrap-table2-toolkit":
        "react-bootstrap-table2-toolkit/dist/react-bootstrap-table2-toolkit.min.js",
      resources: path.join(__dirname, "src", "resources"),
      scenes: path.join(__dirname, "src", "scenes"),
      store: path.join(__dirname, "src", "store"),
      styles: path.join(__dirname, "src", "styles"),
      typings: path.join(__dirname, "src", "typings"),
      utils: path.join(__dirname, "src", "utils"),
    },
    extensions: [".js", ".jsx", ".ts", ".tsx"],
    fallback: {
      buffer: require.resolve("buffer"),
      crypto: require.resolve("crypto-browserify"),
      stream: require.resolve("stream-browserify"),
    },
  },
  stats: {
    children: false,
    colors: true,
    modules: false,
  },
};
