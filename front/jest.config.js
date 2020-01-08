// @ts-check

module.exports = {
  collectCoverage: true,
  coverageDirectory: "coverage",
  coverageReporters: [
    "text",
    "lcov"
  ],
  globals: {
    'ts-jest': {
      tsConfig: {
        allowJs: true,
      }
    }
  },
  moduleNameMapper: {
    "\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$": "<rootDir>/__mocks__/fileMock.js",
    "\\.(css|less)$": "identity-obj-proxy"
  },
  preset: "ts-jest",
  setupFiles: [
    "jest-canvas-mock"
  ],
  setupFilesAfterEnv: [
    "<rootDir>/setup.ts"
  ],
  transform: {
    "^.+\\.(j|t)sx?$": "ts-jest"
  },
  transformIgnorePatterns: [
    "node_modules/(?!react-syntax-highlighter/.*)"
  ],
  verbose: true
};
