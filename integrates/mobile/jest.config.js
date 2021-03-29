// @ts-check

const common = {
  moduleFileExtensions: ["js", "jsx", "ts", "tsx", "mjs"],
  setupFilesAfterEnv: ["<rootDir>/jestSetup.ts"],
  testEnvironment: "jsdom",
  transformIgnorePatterns: ["node_modules/(?!react-router-native)/"],
};

module.exports = {
  collectCoverage: true,
  coverageDirectory: "coverage",
  coverageReporters: ["text", "lcov"],
  projects: [
    { ...common, preset: "jest-expo/ios" },
    { ...common, preset: "jest-expo/android" },
  ],
  verbose: true,
};
