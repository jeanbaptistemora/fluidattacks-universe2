// @ts-check

const isUsingEnzyme = process.env.isEnzyme === "true";
const enzymeTestMatch = ["<rootDir>/**/*.spec.tsx"];
const rtlTestMatch = ["<rootDir>/**/*.test.tsx"];

const common = {
  moduleFileExtensions: ["js", "jsx", "ts", "tsx", "mjs"],
  setupFilesAfterEnv: ["<rootDir>/jestSetup.ts"],
  testEnvironment: "jsdom",
  testMatch: isUsingEnzyme ? enzymeTestMatch : rtlTestMatch,
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
