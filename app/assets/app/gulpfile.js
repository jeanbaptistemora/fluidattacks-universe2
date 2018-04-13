const external_default = require("../externs/externs_default.js");
const externs_default = external_default.functions;
const external_verbose = require("../externs/externs_verbose.js");
const externs_verbose = external_verbose.functions;
const gulp = require("gulp");
const compiler = require("google-closure-compiler-js").gulp();
const options_default = {
  "compilationLevel": "ADVANCED",
  "createSourceMap": true,
  "externs": [{"src": externs_default}],
  "languageIn": "ECMASCRIPT6",
  "processCommonJsModules": true,
  "warningLevel": "DEFAULT"
};
const options_verbose = {
  "compilationLevel": "ADVANCED",
  "createSourceMap": true,
  "env": "BROWSER",
  "externs": [{"src": externs_verbose}],
  "languageIn": "ECMASCRIPT6",
  "processCommonJsModules": true,
  "warningLevel": "VERBOSE"
};

gulp.task("default", function script () {
  return gulp.src([
    "./**/*.js",
    "!./app.js",
    "!./xhr.js",
    "!./login.js",
    "!./externs.js",
    "!./gulpfile.js"
  ]).
    pipe(compiler(options_default));
});

gulp.task("verbose", function script () {
  return gulp.src(["./app.js"]).
    pipe(compiler(options_verbose));
});
