const anyName = require("compression-webpack-plugin");

// must fail line 6
new anyName({
    filename: "[path][base].gz",
    algorithm: "gzip",
    test: /\.js$|\.css$|\.html$/,
    threshold: 10240,
    minRatio: 0.8,
});