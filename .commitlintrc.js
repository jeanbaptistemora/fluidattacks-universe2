module.exports = {
  parserPreset: './.parser-preset',
  extends: ['@commitlint/config-conventional'],
  rules: {
    'header-max-length': [2, 'always', 50], // header max chars 50
    'scope-empty': [2, 'never'], // always scope
    'subject-case': [2, 'always', 'lower-case'], // lower-case subject
    'body-leading-blank': [2, 'always'], // blank line between header and body
    'body-max-line-length': [2, 'always', 72], // body lines max chars 72
    'footer-leading-blank': [2, 'always'], // blank line between body and footer
    'footer-max-line-length': [2, 'always', 72], // footer lines max chars 72
    'type-enum': [2, 'always', [
      'feat',     // New feature
      'perf',     // Improves performance
      'fix',      // Bug fix
      'revert',   // Revert to a previous commit in history
      'docs',     // Documentation only changes
      'style',    // Do not affect the meaning of the code (formatting, etc)
      'refactor', // Neither fixes a bug or adds a feature
      'test',     // Adding missing tests or correcting existing tests
      'sltn'      // Hacking solution
      ]
    ],
    'scope-enum': [2, 'always', [
      'front',  // Front-End change
      'back',   // Back-End change
      'infra',  // Infrastructure change
      'config', // Configuration files change
      'build',  // System component change (ci, scons, webpack...)
      'jobs',   // asynchronous or schedule tasks (backups, maintainance...)
      'cross',  // Mix of two or more scopes
      'sys'     // Systems hacking solution
      ]
    ]
  }
}
