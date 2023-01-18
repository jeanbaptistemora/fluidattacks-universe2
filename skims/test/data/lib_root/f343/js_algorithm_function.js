const CompressionPlugin = require("compression-webpack-plugin");

// must not fail
module.exports = {
  plugins: [
    new CompressionPlugin({
      algorithm(input, compressionOptions, callback) {
        return compressionFunction(input, compressionOptions, callback);
      },
    }),
  ],
};

// Outside an array

new CompressionPlugin({
  algorithm(input, compressionOptions, callback) {
    return compressionFunction(input, compressionOptions, callback);
  },
});
