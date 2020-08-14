// @ts-check

const common = {
  moduleFileExtensions: [
    "js",
    "jsx",
    "ts",
    "tsx",
    "mjs"
  ],
  transformIgnorePatterns: [
    "node_modules/(?!react-router-native)/"
  ],
  setupFilesAfterEnv: [
    "<rootDir>/jestSetup.ts"
  ],
  testEnvironment: "jsdom",
}

module.exports = {
  collectCoverage: true,
  coverageDirectory: "coverage",
  coverageReporters: [
    "text",
    "lcov"
  ],
  projects: [
    { ...common, preset: "jest-expo/ios" },
    { ...common, preset: "jest-expo/android" },
  ],
  verbose: true
}
