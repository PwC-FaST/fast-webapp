const webpack = require('webpack')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const OptimizeCSSPlugin = require('optimize-css-assets-webpack-plugin')
const BundleTracker = require('webpack-bundle-tracker')
const WorkboxPlugin = require('workbox-webpack-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')

const path = require('path')
const fs = require('fs')

const distDir = 'dist/farmer_mobile_app'
const publicPath = '/static/farmer_mobile_app/'

module.exports = {
  context: __dirname,
  entry: {
    main: ['./src/main.js']
  },
  output: {
    path: path.join(__dirname, distDir),
    filename: '[name]-[hash].js',
    chunkFilename: '[name].bundle.js',
    publicPath: publicPath
  },
  resolve: {
    extensions: ['.wasm', '.mjs', '.js', '.vue', '.json'],
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      '@': path.resolve(__dirname, 'src')
    },
    modules: [
      path.join(__dirname, 'src'),
      path.resolve(__dirname, 'node_modules')
    ]
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: 'babel-loader',
        include: [
          path.join(__dirname, 'src'),
          path.join(__dirname, 'node_modules/framework7'),
          path.join(__dirname, 'node_modules/framework7-vue'),
          path.join(__dirname, 'node_modules/template7'),
          path.join(__dirname, 'node_modules/dom7'),
          path.join(__dirname, 'node_modules/pwacompat'),
          path.join(__dirname, 'node_modules/vue-moment-lib'),
          path.join(__dirname, 'node_modules/vuex-persist'),
          path.join(__dirname, 'node_modules/vue2-leaflet-vectorgrid'),
          path.join(__dirname, 'node_modules/plotty'),
        ]
      },
      {
        test: /\.vue$/,
        use: 'vue-loader'
      },
      {
        test: /\.mjs$/,
        include: /node_modules/,
        type: 'javascript/auto'
      },
      {
        test: /\.(graphql|gql)$/,
        exclude: /node_modules/,
        loader: 'graphql-tag/loader'
      },
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader'
        ]
      },
      {
        test: /\.styl(us)?$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'stylus-loader'
        ]
      },
      {
        test: /\.less$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'less-loader'
        ]
      },
      {
        test: /\.(png|jpe?g|gif)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: 'images/[name].[hash:7].[ext]'
        }
      },
      {
        test: /\.svg$/,
        oneOf: [
          {
            resourceQuery: /inline/,
            loader: 'vue-svg-loader'
          },
          {
            loader: 'file-loader',
            query: {
              name: 'assets/[name].[hash:8].[ext]'
            }
          }
        ]
      },
      {
        test: /\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: 'media/[name].[hash:7].[ext]'
        }
      },
      {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: 'fonts/[name].[hash:7].[ext]'
        }
      }
    ]
  }
}

const staticFilesToCopy = [
  {from: 'src/favicon.ico', to: 'favicon.ico', toType: 'file'},
  {from: 'src/icons', to: 'icons', toType: 'dir'},
  {from: 'src/img', to: 'img', toType: 'dir'},
  {from: 'src/manifest.webmanifest', to: 'manifest.webmanifest', toType: 'file'},
  {from: 'src/embedded.html', to: 'embedded.html', toType: 'file'}
]

if (process.env.NODE_ENV === 'production') {
  console.log('Loading production environment')
  module.exports.mode = 'production'
  module.exports.devtool = '#source-map'

  module.exports.plugins = [
    new CleanWebpackPlugin([path.join(__dirname, distDir)]),
    new webpack.DefinePlugin({'FAST_ENVIRONMENT': JSON.stringify('production')}),
    new BundleTracker({filename: path.join('.', distDir, 'webpack-stats.json')}),
    new CopyWebpackPlugin(staticFilesToCopy),
    new HtmlWebpackPlugin({
      hash: false,
      template: './src/index.html',
      filename: 'index.html'
    }),
    new UglifyJsPlugin({uglifyOptions: {compress: {warnings: false}}, sourceMap: true, parallel: true}),
    new OptimizeCSSPlugin({cssProcessorOptions: {safe: true, map: {inline: false}}}),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NamedModulesPlugin(),
    new VueLoaderPlugin(),
    new webpack.HashedModuleIdsPlugin(),
    new webpack.optimize.ModuleConcatenationPlugin(),
    new MiniCssExtractPlugin({filename: 'main.css'}),
    new WorkboxPlugin.GenerateSW({
      clientsClaim: true,
      skipWaiting: true
    })
  ]

} else {
  console.log('Loading development environment')
  module.exports.mode = 'development'
  module.exports.devtool = '#eval-source-map'
  module.exports.plugins = [
    new CleanWebpackPlugin([path.join(__dirname, distDir)]),
    new webpack.DefinePlugin({'FAST_ENVIRONMENT': JSON.stringify('development')}),
    new BundleTracker({filename: path.join('.', distDir, 'webpack-stats.json')}),
    new CopyWebpackPlugin(staticFilesToCopy),
    new webpack.SourceMapDevToolPlugin(),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NamedModulesPlugin(),
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin({filename: 'main.css'})
  ]

  module.exports.watch = true

}

