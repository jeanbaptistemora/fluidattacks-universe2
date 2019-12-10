/* Webpack plugins */
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
let CommonConfig = require('./webpack.common.config');

/* Webpack production configs definition */
CommonConfig.plugins = CommonConfig.plugins.concat([
  new OptimizeCssAssetsPlugin()
]);

module.exports = {
  ...CommonConfig,
  stats: {
    children: false,
    warnings: false
  },
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin()],
  }
}
