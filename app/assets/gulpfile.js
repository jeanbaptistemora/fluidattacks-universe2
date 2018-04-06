var gulp = require('gulp');
const compiler = require('google-closure-compiler-js').gulp();

gulp.task('script', function() {
  return gulp.src(['/usr/src/app/app/assets/app/**/*.js', '!/usr/src/app/app/assets/app/xhr.js', '!/usr/src/app/app/assets/app/login.js'], {base: 'app/'})
      .pipe(compiler({
          compilationLevel: 'SIMPLE',
          warningLevel: 'DEFAULT',
          checksOnly: true,
        }))
});
