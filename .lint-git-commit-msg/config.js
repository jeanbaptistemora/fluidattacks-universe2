const HEADER_LENGTH_MAX = 72;
const LINE_LENGTH_MAX = 72;
const BODY_LENGTH_MIN = 15;

module.exports = {
  parserPreset: "./.commitlint-parser-preset",
  rules: {
    // Body
    "body-leading-blank": [2, "always"], // blank line between header and body
    "body-empty": [2, "never"], // body cannot be empty
    "body-max-line-length": [2, "always", LINE_LENGTH_MAX], // body lines max chars LINE_LENGTH_MAX
    "body-min-length": [2, "always", BODY_LENGTH_MIN], // body more than BODY_LENGTH_MIN chars

    // Footer
    "footer-leading-blank": [2, "always"], // blank line between body and footer
    "footer-max-line-length": [2, "always", LINE_LENGTH_MAX], // footer lines max chars LINE_LENGTH_MAX

    // Header
    "header-case": [2, "always", "lower-case"], // header lower case
    "header-max-length": [2, "always", HEADER_LENGTH_MAX], // header max chars HEADER_LENGTH_MAX

    // Scope
    "scope-empty": [2, "never"], // scope always
    "scope-enum": [
      2,
      "always",
      [
        "front", // Front-End change
        "back", // Back-End change
        "infra", // Infrastructure change
        "conf", // Configuration files change
        "build", // System component change (ci, scons, webpack...)
        "job", // asynchronous or schedule tasks (backups, maintainance...)
        "cross", // Mix of two or more scopes
        "doc", // Documentation only changes
      ],
    ],

    // Subject (commit title without type and scope)
    "subject-case": [2, "always", "lower-case"], // subject lower-case
    "subject-empty": [2, "never"], // subject always

    // Type
    "type-empty": [2, "never"], //type always
    "type-enum": [
      2,
      "always",
      [
        "feat", // New feature
        "perf", // Improves performance
        "fix", // Bug fix
        "rever", // Revert to a previous commit in history
        "style", // Do not affect the meaning of the code (formatting, etc)
        "refac", // Neither fixes a bug or adds a feature
        "test", // Adding missing tests or correcting existing tests
      ],
    ],
  },
};
