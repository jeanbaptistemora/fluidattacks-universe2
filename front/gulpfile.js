/* Gulp-cli */
var gulp = require("gulp");
/* Compile typescript */
var ts = require("gulp-typescript");
/* Webpack Serverside JS to Clientside JS */
var browserify = require("browserify");
/* Use tsconfig json */
var tsProject = ts.createProject("tsconfig.json");
var tsLogin = ts.createProject("./../app/assets/login/tsconfig.json");
var source = require('vinyl-source-stream')
/* Defined constants */
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
 * Main compile task
 */
const compile = () => {
  return tsProject.src()
    .pipe(tsProject())
    .js.pipe(gulp.dest("./build"));
};
gulp.task("compile", compile);
/**
 * Main package task
 */
const package = () => {
  return browserify({
    entries: [paths.dashboard.source],
    debug: true
  }).bundle()
    .pipe(source(paths.dashboard.browser))
    .pipe(gulp.dest(paths.dashboard.destination));
};
gulp.task(
  "package", 
  ['compile'], 
  package
);
/**
 * Temporary task before full react integration
 */
const compileLogin = () => {
  return tsLogin.src()
  .pipe(tsLogin())
  .js.pipe(gulp.dest(paths.login.destination));
};
gulp.task("compile-login", compileLogin);
/**
 * Temporary task before react full integration
 */
const packageLogin = () => {
  return browserify({
    entries: [paths.login.source],
    debug: true
  }).bundle()
    .pipe(source(paths.login.browser))
    .pipe(gulp.dest(paths.login.destination));
};
gulp.task(
  "package-login", 
  ["compile-login"],
  packageLogin
);
 /**
  * BuildTask
  */
gulp.task(
  'integrates', 
  ["package-login", "package"]
);
gulp.task(
  'default',
  ['integrates']
);