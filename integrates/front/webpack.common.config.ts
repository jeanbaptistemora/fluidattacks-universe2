import MiniCssExtractPlugin from "mini-css-extract-plugin";
import path from "path";
import webpack from "webpack";

export const commonConfig: webpack.Configuration = {
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
    ],
  },
  output: {
    filename: "[name]-bundle.min.js",
    futureEmitAssets: true,
    path: path.resolve(__dirname, "../app/static/dashboard/"),
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name]-style.min.css",
    }),
    new webpack.EnvironmentPlugin([
      "CI_COMMIT_SHA",
      "CI_COMMIT_SHORT_SHA",
      "FI_VERSION",
    ]),
  ],
  resolve: {
    alias: {
      components: path.join(__dirname, "src", "components"),
      graphics: path.join(__dirname, "src", "graphics"),
      resources: path.join(__dirname, "src", "resources"),
      scenes: path.join(__dirname, "src", "scenes"),
      store: path.join(__dirname, "src", "store"),
      styles: path.join(__dirname, "src", "styles"),
      typings: path.join(__dirname, "src", "typings"),
      utils: path.join(__dirname, "src", "utils"),
    },
    extensions: [".js", ".jsx", ".ts", ".tsx"],
  },
  stats: {
    children: false,
    colors: true,
    modules: false,
  },
};
