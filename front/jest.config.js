// @ts-check

module.exports = {
  collectCoverage: true,
  collectCoverageFrom: [
    "src/**/*.{ts,tsx,js,jsx}",
    "!**/node_modules/**",
    "!**/*.d.ts",
    "!src/**/*.spec.tsx"
  ],
  coverageDirectory: "coverage",
  coverageReporters: [
    "text",
    "lcov"
  ],
  moduleFileExtensions: [
    "ts",
    "tsx",
    "js",
    "jsx"
  ],
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
    "^.+\\.tsx?$": "ts-jest"
  },
  transformIgnorePatterns: [
    "node_modules/*"
  ],
  testRegex: [
    "(src/components/.*/index\\.spec\\.tsx)$",
    "(src/scenes/Dashboard/.*/.*/index\\.spec\\.tsx)$",
    "src/scenes/Dashboard/containers/ProjectUsersView/AddUserModal/index.spec.tsx",
    "src/scenes/Login/containers/Access/index.spec.tsx",
    "src/scenes/Registration/components/CompulsoryNotice/index.spec.tsx",
    "src/scenes/Registration/containers/WelcomeView/index.spec.tsx",
    "src/scenes/Dashboard/index.spec.tsx",
    "src/utils/forms/index.spec.tsx",
    "src/utils/index.spec.tsx"
  ],
  verbose: true
};
