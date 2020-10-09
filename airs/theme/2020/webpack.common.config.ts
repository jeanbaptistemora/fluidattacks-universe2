import path from "path";
import webpack from "webpack";

export const commonConfig: webpack.Configuration = {
  entry: {
    anchor: "./static/js/anchor.ts",
    cardHover: "./static/js/cardHover.ts",
    carousel: "./static/js/carousel.ts",
    contactSlides: "./static/js/contactSlides.ts",
    contentHome: "./static/js/contentHome.ts",
    defends: "./static/js/defends.ts",
    dynClasses: "./static/js/dynClasses.ts",
    form: "./static/js/form.ts",
    faqGen: "./static/js/faqGen.ts",
    menu: "./static/js/menu.ts",
    navbar: "./static/js/navbar.ts",
    progressBar: "./static/js/progressBar.ts",
    rules: "./static/js/rules.ts",
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
