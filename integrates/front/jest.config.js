/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

const esModules = [
  "react-syntax-highlighter",
  "react-markdown",
  "vfile",
  "unist-.+",
  "unified",
  "bail",
  "is-plain-obj",
  "trough",
  "remark-.+",
  "mdast-util-.+",
  "micromark",
  "parse-entities",
  "character-entities",
  "property-information",
  "comma-separated-tokens",
  "space-separated-tokens",
  "ccount",
  "escape-string-regexp",
  "markdown-table",
  "hast-util-.+",
  "rehype-.+",
  "hastscript",
  "web-namespaces",
  "hast-to-hyperscript",
  "zwitch",
  "html-void-elements",
  "direction",
  "bcp-47-match",
  "rehype",
  "stringify-entities",
  "decode-named-character-reference",
  "refractor",
  "character-reference-invalid",
  "is-decimal",
  "is-hexadecimal",
  "is-alphanumerical",
  "is-alphabetical",
  "trim-lines",
].join("|");

module.exports = {
  collectCoverage: true,
  coverageDirectory: "coverage",
  coverageReporters: ["text", "lcov"],
  globals: {
    "ts-jest": {
      isolatedModules: true,
      tsconfig: {
        allowJs: true,
      },
    },
  },
  moduleDirectories: ["node_modules", "src"],
  moduleNameMapper: {
    "\\.(css|less)$": "identity-obj-proxy",
    "\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$":
      "<rootDir>/__mocks__/fileMock.js",
  },
  preset: "ts-jest",
  setupFiles: ["jest-canvas-mock"],
  setupFilesAfterEnv: ["<rootDir>/jestSetup.ts"],
  testEnvironment: "jest-environment-jsdom",
  transform: {
    [`(${esModules}).+\\.js$`]: "babel-jest",
  },
  transformIgnorePatterns: [
    `[/\\\\]node_modules[/\\\\](?!${esModules}).+\\.(js|jsx|mjs|cjs|ts|tsx)$`,
  ],
  verbose: true,
};
