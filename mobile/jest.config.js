// @ts-check

module.exports = {
  collectCoverage: true,
  coverageReporters: [
    "text"
  ],
  preset: "jest-expo",
  transformIgnorePatterns: [
    "node_modules/?!(react-router-native)"
  ],
  verbose: true
}
