import CompressionPlugin from "compression-webpack-plugin";

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
