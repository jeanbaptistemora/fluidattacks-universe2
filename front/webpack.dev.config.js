let CommonConfig = require('./webpack.common.config');
const webpack = require('webpack');

/* Webpack development configs definition */
CommonConfig.plugins = CommonConfig.plugins.concat([
  new webpack.ProgressPlugin()
]);

module.exports = {
  ...CommonConfig,
  optimization: {
     minimize: false
  }
}
