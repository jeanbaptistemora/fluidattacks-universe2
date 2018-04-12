const gulp = require("gulp");
const compiler = require("google-closure-compiler-js").gulp();
const options = {
  "checksOnly": true,
  "compilationLevel": "ADVANCED",
  "createSourceMap": true,
  "externs": "usr/src/app/app/assets/externs/externs.js",
  "languageIn": "ECMASCRIPT6",
  "processCommonJsModules": true,
  "warningLevel": "DEFAULT"
};
// './app/**/*.js'
gulp.task("script", function () {
  return gulp.src([
    ".app/**/*.js",
    "!./login.js",
    "!./app.js",
    "!./xhr.js",
    "!./gulpfile.js"
  ]).
    pipe(compiler(options));
});
