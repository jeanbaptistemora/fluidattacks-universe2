/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

const esModules = [
  "bcp-47-match",
  "ccount",
  "character-entities-html4",
  "decode-named-character-reference",
  "direction",
  "hast-util-.+",
  "markdown-table",
  "mdast-util-.+",
  "micromark",
  "react-markdown",
  "rehype-.+",
  "rehype",
  "remark-.+",
  "stringify-entities",
  "trim-lines",
  "unist-.+",
].join("|");

module.exports = {
  bail: 1,
  collectCoverage: true,
  coverageDirectory: "coverage",
  coverageReporters: ["text", "lcov"],
  coverageThreshold: {
    global: {
      branches: 58,
    },
  },
  maxWorkers: 1,
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
    [`(${esModules}).*\\.js$`]: "babel-jest",
  },
  transformIgnorePatterns: [`[/\\\\]node_modules[/\\\\](?!${esModules})/`],
};
