// @ts-check

module.exports = {
  collectCoverage: true,
  coverageDirectory: "coverage",
  coverageReporters: [
    "text",
    "lcov"
  ],
  preset: "jest-expo",
  setupFilesAfterEnv: [
    "<rootDir>/jestSetup.ts"
  ],
  testEnvironment: "jsdom",
  transformIgnorePatterns: [
    "node_modules/?!(react-router-native)"
  ],
  verbose: true
}
