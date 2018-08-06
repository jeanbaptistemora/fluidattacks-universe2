/* Webpack plugins */
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
/* Webpack common module definition */
module.exports = {
  entry: "./src/index.js",
  output: {
    filename: 'bundle.min.js'
  },
  module: {
    rules: [{ 
      test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
      loader: "url-loader?limit=10000&mimetype=application/font-woff&name=fonts/[hash].[ext]"
    }, { 
      test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, 
      loader: "file-loader",
      options: {
        name: 'fonts/[hash].[ext]'
      }
    }, {
      test: /\.(png|jpg|gif)$/,
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
    },{
      test: /\.css$/,
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
    new UglifyJsPlugin(),
    new ExtractTextPlugin("integrates.min.css"),
    new OptimizeCssAssetsPlugin()
  ],
  stats: {
    children: false,
    warnings: false
  }
}
