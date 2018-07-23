/* Webpack plugins */
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
/* Webpack common module definition */
module.exports = {
  entry: "./scenes/index.js",
  output: {
    filename: 'bundle.min.js'
  },
  module: {
    rules: [{
      test: /\.css$/,
      use: ExtractTextPlugin.extract({
        fallback: "style-loader",
        use: "css-loader"
      })
    }]
  },
  plugins: [
    new UglifyJsPlugin(),
    new ExtractTextPlugin("integrates.min.css"),
    new OptimizeCssAssetsPlugin()
  ],
  stats: {
    children: false,
    warnings: false
  }
}