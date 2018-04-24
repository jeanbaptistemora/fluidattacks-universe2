const externalVerbose = require("../externs/externs_verbose.js");
const externsVerbose = externalVerbose.functions;
const gulp = require("gulp");
const compiler = require("google-closure-compiler-js").gulp();

const optionsVerbose = {
  "compilationLevel": "ADVANCED",
  "createSourceMap": true,
  "env": "BROWSER",
  "externs": [{"src": externsVerbose}],
  "languageIn": "ECMASCRIPT6",
  "processCommonJsModules": true,
  "warningLevel": "VERBOSE"
};

gulp.task("verbose", () => gulp.src([
  "./**/*.js",
  "!./gulpfile.js",
  "!./xhr.js",
  "!./login.js",
  "./translationParameters.js"
]).
  pipe(compiler(optionsVerbose)));
