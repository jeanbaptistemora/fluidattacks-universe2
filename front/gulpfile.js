/* Module used to control gulp tasks */
var gulp = require("gulp");
/* Module used under css type task */
var css = require('gulp-typed-css-modules');
/* Modules used under package task */
var webpack = require('webpack');
var gulpWebpack = require('webpack-stream');
var gulpPlumber = require('gulp-plumber');
/* Modules used under compilation task */
var ts = require("gulp-typescript");
var tsProject = ts.createProject("tsconfig.json");
/* Output filenames and paths */
var paths = {
  dashboard: {
    source: './build/index.js',
    browser: 'bundle.min.js',
    destination: './../app/assets/dashboard'
  }
};
/**
 * CSS Types Task: Custom CSS Types definition
 * Create css.d.ts before compilation
 * it's used to import css modules on react
 */
gulp.task('css', function(){
    return gulp.src(["./src/**/*.css"])
    .pipe(css())
    .pipe(gulp.dest("./src"));
});
/**
 * Compile Task: Typescript Compilation
 * Compile all .ts files in javascript server files
 */
gulp.task(
  "compile",
  ['css'],
  () => {
    return tsProject.src()
      .pipe(gulpPlumber())
      .pipe(tsProject())
      .js.pipe(gulp.dest("./src"));
  }
);
/**
 * Package Task: Use webpack
 * it converts JS from serverside to clientside
 * it adds and minifies CSS
 */
gulp.task(
  "package:prod",
  ['compile'],
  () => {
    return gulp.src('./src/index.js')
      .pipe(gulpWebpack(require('./webpack.prod.config.js'), webpack))
      .pipe(gulp.dest(paths.dashboard.destination));
  }
);

gulp.task(
  "package:dev",
  ['compile'],
  () => {
    return gulp.src('./src/index.js')
      .pipe(gulpWebpack(require('./webpack.dev.config.js'), webpack))
      .pipe(gulp.dest(paths.dashboard.destination));
  }
);
/**
 * Development Task: Code watcher
 * Run package task when a file change
 */
gulp.task('watch', ['package:dev'], function() {
  gulp.watch(['./src/**/*.ts', './src/**/*.tsx'], ['package:dev']);
});
/**
* Integrates Task: Bundle integrates front
* Packages all compiled react components and styles
* Minifies and uglifies the resulting JS
*/
gulp.task("integrates", ["package:prod"]);
/**
 * Default Task: Run Integrates Task
 */
gulp.task("default", ["integrates"]);
