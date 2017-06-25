var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  context: __dirname,
  entry: [
      'react-hot-loader/patch',
      'webpack-dev-server/client?http://0.0.0.0:3000',
      'webpack/hot/only-dev-server',
      './itineraryplanner/static/js/index',
  ],
  output: {
      path: path.resolve('./itineraryplanner/static/bundles/'),
      filename: '[name]-[hash].js',
      publicPath: 'http://0.0.0.0:3000/static/bundles/', // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name
  },

  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoEmitOnErrorsPlugin(), // don't reload if there is an error
    new BundleTracker({filename: './itineraryplanner/webpack-stats.json'}),
  ],
   module: {
    rules: [
      // we pass the output from babel loader to react-hot loader
      { 
        test: /\.jsx?$/, 
        exclude: /node_modules/, 
        loaders: ['babel-loader'], 
      },
    ],
  },
  resolve: {
    modules: ["node_modules"],
    extensions: ["*", ".js", ".jsx"]
  }
};
// TODO: https://github.com/ezhome/django-webpack-loader
// https://webpack.js.org/concepts/
// https://gist.github.com/Belgabor/130e7770575e74581b67597fcb61717e
// https://github.com/jansoren/react-webpack-tutorial