import { ResourceLanguage } from "i18next";

export const enTranslations: ResourceLanguage = {
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
    diff: "Compared to last week",
    greetingText: "Welcome",
    remediated: "Remediated vulnerabilities",
    vulnsFound: "of <0>{{totalVulns}}</0> found in <0>{{count}}</0> system",
    vulnsFound_plural: "of <0>{{totalVulns}}</0> found in <0>{{count}}</0> systems",
  },
  lock: {
    btn: "Authenticate",
    title: "Unlock to continue",
  },
  login: {
    btnGoogleText: "Sign in with Google",
    btnMicrosoftText: "Sign in with Microsoft",
    newVersion: {
      btn: "Update",
      content: "Get the latest features and improvements",
      title: "New version available",
    },
  },
  welcome: {
    greetingText: "Hello",
  },
};
