/* Module used to control gulp tasks */
var gulp = require("gulp");
/* Module used under css type task */
var css = require('gulp-typed-css-modules');
/* Modules used under package task */
var browserify = require("browserify");
var webpack = require('webpack');
var gulpWebpack = require('webpack-stream');
/* Modules used under compilation task */
var ts = require("gulp-typescript");
var tsProject = ts.createProject("tsconfig.json");
var tsLogin = ts.createProject("./../app/assets/login/tsconfig.json");
var source = require('vinyl-source-stream')
/* Output filenames and paths */
var paths = {
  dashboard: {
    source: './build/index.js',
    browser: 'bundle.min.js',
    destination: './../app/assets/dashboard'
  },
  login: {
    source: './../app/assets/login/index.js',
    browser: 'bundle.min.js',
    destination: './../app/assets/login'
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
  "package", 
  ['compile'], 
  () => {
    return gulp.src('./src/index.js')
      .pipe(gulpWebpack(require('./webpack.config.js'), webpack))
      .pipe(gulp.dest(paths.dashboard.destination));
  }
);
/**
 * Temporary Task: Typescript Compilation (Login)
 * Compile login, it's a temporary task while
 * integrate's migration is done
 */
gulp.task(
  "compile-login",
  () => {
    return tsLogin.src()
    .pipe(tsLogin())
    .js.pipe(gulp.dest(paths.login.destination));
  }
);
/**
 * Temporary Task: Use browserify (Login)
 * it converts JS from serverside to clientside
 */
gulp.task(
  "package-login", 
  ["compile-login"],
  () => {
    return browserify({
      entries: [paths.login.source],
      debug: true
    }).bundle()
      .pipe(source(paths.login.browser))
      .pipe(gulp.dest(paths.login.destination));
  }
);
/**
 * Development Task: Code's watcher
 * Run package's steps when a file change
 */
gulp.task('watch', ['package'], function() {
  gulp.watch('./src/**/*.ts', ['package']);
});
/**
* Integrate's Task: Deploy React App
* Deploy dashboard and login
* "login" is a temporary task before full integration
*/
gulp.task("integrates", ["package-login", "package"]);
/**
 * Default Task: Run Integrate's Task
 */
gulp.task("default", ["integrates"]);
