/* Webpack plugins */
const ExtractTextPlugin = require("extract-text-webpack-plugin");

/* Webpack common module definition */
module.exports = {
  entry: {
    main: "./src/index.js",
    dashboard: "./src/scenes/Dashboard/index.js"
  },
  output: {
    filename: '[name]-bundle.min.js'
  },
  module: {
    rules: [{
      test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
      loader: "url-loader?limit=10000&mimetype=application/font-woff&name=fonts/[hash].[ext]"
    }, {
      test: /\.(ttf|eot)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
      loader: "file-loader",
      options: {
        name: 'fonts/[hash].[ext]'
      }
    }, {
      test: /\.(png|jpg|gif|svg)$/,
      use: [{
        loader: 'file-loader',
        options: {
          name: '[hash].[ext]',
          outputPath: 'img/',
          publicPath: 'assets/dashboard/img/'
        }
      }]
    }, {
      test: /\.tsx?$/,
      loader: "awesome-typescript-loader"
    }, {
      test: /\.css$/,
      include: /node_modules/,
      use: ExtractTextPlugin.extract({
        use: [{
          loader: 'css-loader'
        }]
      })
    }, {
      test: /\.css$/,
      exclude: /node_modules/,
      use: ExtractTextPlugin.extract({
        use: [{
          loader: 'css-loader',
          options: {
            modules: true
          }
        }]
      })
    }]
  },
  plugins: [
    new ExtractTextPlugin("[name]-style.min.css")
  ],
  stats: {
    children: false,
    warnings: false
  }
}
