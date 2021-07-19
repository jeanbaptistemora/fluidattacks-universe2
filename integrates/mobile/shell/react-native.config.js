/* eslint-disable @typescript-eslint/no-require-imports */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-var-requires */
/* eslint-disable @typescript-eslint/restrict-template-expressions */
/* eslint-disable import/no-extraneous-dependencies */
const android = require("@react-native-community/cli-platform-android");

module.exports = {
  platforms: {
    android: {
      dependencyConfig: android.dependencyConfig,
      linkConfig: android.linkConfig,
      projectConfig: android.projectConfig,
    },
  },
  project: {
    android: {
      buildGradlePath: "app/build.gradle",
    },
  },
  reactNativePath: "versioned-react-native",
};
