/* Webpack plugins */
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
let CommonConfig = require('./webpack.common.config');

/* Webpack production configs definition */
CommonConfig.plugins = CommonConfig.plugins.concat([
  new UglifyJsPlugin({ parallel: true }),
  new OptimizeCssAssetsPlugin()
]);

module.exports = {
  ...CommonConfig,
  stats: {
    children: false,
    warnings: false
  }
}
