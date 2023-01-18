const CompressionPlugin = require("compression-webpack-plugin");

// must fail line 4
new CompressionPlugin({
  filename: "[path][base].gz",
  test: /\.js$|\.css$|\.html$/,
  threshold: 10240,
  minRatio: 0.8,
});
