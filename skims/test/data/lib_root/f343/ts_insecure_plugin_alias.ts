import CompressionPlugin from "compression-webpack-plugin";

// Must fail line 6
new CompressionPlugin({
    filename: "[path][base].gz",
    algorithm: "gzip",
    test: /\.js$|\.css$|\.html$/,
    threshold: 10240,
    minRatio: 0.8,
});

const pluginOpts = {
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

new CompressionPlugin(pluginOpts);

const pluginOpts2 = {
    filename: "[path][base].gz",
    algorithm: "gzip",
    test: /\.js$|\.css$|\.html$/,
    threshold: 10240,
    minRatio: 0.8,
  };

new CompressionPlugin(pluginOpts2);
