module.exports = {
  parserPreset: './.commitlint-parser-preset',
  extends: [ '@commitlint/config-conventional' ],
  rules: {
    'header-max-length': [ 2, 'always', 60 ], // header max chars 60
    'scope-empty': [ 2, 'never' ], // always scope
    'subject-case': [ 2, 'always', 'lower-case' ], // lower-case subject
    'body-leading-blank': [ 2, 'always' ], // blank line between header and body
    'body-max-line-length': [ 2, 'always', 72 ], // body lines max chars 72
    'footer-leading-blank': [ 2, 'always' ], // blank line between body and footer
    'footer-max-line-length': [ 2, 'always', 72 ], // footer lines max chars 72
    'type-enum': [
      2,
      'always',
      [
        'feat', // New feature
        'perf', // Improves performance
        'fix', // Bug fix
        'rever', // Revert to a previous commit in history
        'style', // Do not affect the meaning of the code (formatting, etc)
        'refac', // Neither fixes a bug or adds a feature
        'test', // Adding missing tests or correcting existing tests
      ],
    ],
    'scope-enum': [
      2,
      'always',
      [
        'front', // Front-End change
        'back', // Back-End change
        'infra', // Infrastructure change
        'conf', // Configuration files change
        'build', // System component change (ci, scons, webpack...)
        'job', // asynchronous or schedule tasks (backups, maintainance...)
        'cross', // Mix of two or more scopes
        'doc', // Documentation only changes
      ],
    ],
  },
};
