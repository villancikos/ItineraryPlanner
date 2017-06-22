var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  context: __dirname,
  entry: [
    'webpack-dev-server/client?http://localhost:3000',
      'webpack/hot/only-dev-server',
      './itineraryplanner/static/js/index',
  ],
  output: {
      path: path.resolve('./itineraryplanner/static/bundles/'),
      filename: '[name]-[hash].js',
      publicPath: 'http://localhost:3000/static/bundles/', // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name
  },

  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoEmitOnErrorsPlugin(), // don't reload if there is an error
    new BundleTracker({filename: './webpack-stats.json'}),
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
