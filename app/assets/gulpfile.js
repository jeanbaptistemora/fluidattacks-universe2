var gulp = require('gulp');
const compiler = require('google-closure-compiler-js').gulp();
var options = {
	compilationLevel: 'SIMPLE',
  createSourceMap: true,
  externs:[
		'./externs.js'
	],
	checksOnly: false,
  processCommonJsModules: true,
	warningLevel: 'DEFAULT',
};
gulp.task('script', function() {
  return gulp.src(['./app/**/*.js', '!./app/login.js', '!./app/xhr.js'], {base: './'})
      .pipe(compiler(options))
});
