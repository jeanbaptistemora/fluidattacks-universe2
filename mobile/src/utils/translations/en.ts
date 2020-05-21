import { ResourceLanguage } from "i18next";

export const enTranslations: ResourceLanguage = {
  common: {
    error: {
      msg: "There is an error :(",
      title: "Oops!",
    },
    logout: "Logout",
    slogan: "We hack your software",
  },
  login: {
    authLoadingText: "Authenticating...",
    btnGoogleText: "Sign in with Google",
    newVersion: {
      btn: "Update",
      content: "Get the latest features and improvements",
      title: "New version available",
    },
  },
  menu: {
    greetingText: "Welcome",
    remediated: "Remediated vulnerabilities",
    vulnsFound: "from <0>{{totalVulns}}</0> found in <0>{{count}}</0> system",
    vulnsFound_plural: "from <0>{{totalVulns}}</0> found in <0>{{count}}</0> systems",
  },
  welcome: {
    greetingText: "Hello",
    unauthorized: "You do not have authorization for login yet. "
      + "Please contact Fluid Attacks's staff or your project administrator to get access.",
  },
};
