import type { ResourceLanguage } from "i18next";

export const enTranslations: ResourceLanguage = {
  about: {
    bin: "Bin:",
    commit: "Commit:",
    deploymentDate: "Deploy Date:",
    licenses: {
      btn: "Done",
      text: "Licenses",
      title: "Third-party licenses",
    },
  },
  common: {
    error: {
      msg: "There is an error :(",
      title: "Oops!",
    },
    logout: "Logout",
    networkError: {
      msg: "Check your network connection and try again",
      title: "Offline",
    },
    sessionExpired: {
      msg: "Your have been logged out",
      title: "Session expired",
    },
    slogan: "We hack your software",
  },
  dashboard: {
    diff: "Compared to last rolling week",
    remediated: "Remediated vulnerabilities",
    vulnsFound: "of <0>{{totalVulns}}</0> found in <0>{{count}}</0> group",
    // eslint-disable-next-line camelcase -- Suffix "_plural" used by i18next lib
    vulnsFound_plural:
      "of <0>{{totalVulns}}</0> found in <0>{{count}}</0> groups",
  },
  lock: {
    btn: "Authenticate",
    title: "Unlock to continue",
  },
  login: {
    btnBitbucketText: "Sign in with Bitbucket",
    btnGoogleText: "Sign in with Google",
    btnMicrosoftText: "Sign in with Microsoft",
    newVersion: {
      btn: "Update",
      content: "Get the latest features and improvements",
      title: "New version available",
    },
  },
  root: {
    msg: "This device cannot be trusted to run the app safely",
    title: "Insecure device",
  },
  welcome: {
    greetingText: "Hello",
  },
};
