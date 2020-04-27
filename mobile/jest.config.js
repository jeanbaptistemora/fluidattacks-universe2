// @ts-check

module.exports = {
  collectCoverage: true,
  coverageReporters: [
    "text"
  ],
  preset: "jest-expo",
  setupFilesAfterEnv: [
    "<rootDir>/jestSetup.ts"
  ],
  transformIgnorePatterns: [
    "node_modules/?!(react-router-native)"
  ],
  verbose: true
}
