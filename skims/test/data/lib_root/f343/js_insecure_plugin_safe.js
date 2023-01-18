const CompressionPlugin = require("compression-webpack-plugin");

// must fail line 6
const opt = {
  filename: "[path][base].gz",
  algorithm: "gzip",
  test: /\.js$|\.css$|\.html$/,
  threshold: 10240,
  minRatio: 0.8,
};

new CompressionPlugin(opt);

// safe
const opt2 = {
  filename: "[path][base].br",
  algorithm: "brotliCompress",
  test: /\.(js|css|html|svg)$/,
  compressionOptions: {
    params: {
      [zlib.constants.BROTLI_PARAM_QUALITY]: 11,
    },
  },
  threshold: 10240,
  minRatio: 0.8,
};

new CompressionPlugin(opt2);
