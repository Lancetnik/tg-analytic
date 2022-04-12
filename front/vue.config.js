const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],

  outputDir: process.env.NODE_ENV === 'production' ? '../backend/app/index/static' : 'dist/',
  // Все ниже - относительно outputDir
  indexPath: process.env.NODE_ENV === 'production' ? '../templates/index.html' : 'index.html',
  assetsDir: '',
  publicPath: process.env.NODE_ENV === 'production' ? 'static' : '/',
})
