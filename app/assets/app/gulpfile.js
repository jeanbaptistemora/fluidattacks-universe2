const external_verbose = require("../externs/externs_verbose.js");
const externs_verbose = external_verbose.functions;
const gulp = require("gulp");
const compiler = require("google-closure-compiler-js").gulp();

const options_verbose = {
  "compilationLevel": "ADVANCED",
  "createSourceMap": true,
  "env": "BROWSER",
  "externs": [{"src": externs_verbose}],
  "languageIn": "ECMASCRIPT6",
  "processCommonJsModules": true,
  "warningLevel": "VERBOSE"
};

gulp.task("verbose", function script () {
  return gulp.src([
    "./**/*.js",
    "!./gulpfile.js",
    "!./xhr.js",
    "!./login.js"
  ]).
    pipe(compiler(options_verbose));
});
