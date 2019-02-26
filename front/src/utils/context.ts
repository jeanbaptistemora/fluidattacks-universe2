export let PRODUCTION_URL: string;
PRODUCTION_URL = "https://fluidattacks.com";

export let REVIEW_URL_PATTERN: string;
REVIEW_URL_PATTERN = ".integrates.env";

export let DEVELOPMENT_URL: string;
DEVELOPMENT_URL = "https://localhost";

export const getEnvironment: (() => string) = (): string => {
  let environment: string;
  /* tslint:disable-next-line:strict-type-predicates
   * Disabling this rule is necessary because the following expression is
   * misbelived to be always true by the linter while it is necessary for
   * avoiding errors in the npm test environment where the object window
   * doesn't exist.
   */
  if (typeof window === "undefined") {
    environment = "development";
  } else {
    const currentUrl: string = window.location.href;
    if (currentUrl.indexOf(DEVELOPMENT_URL) !== -1 || currentUrl === "about:blank") {
      environment = "development";
    } else if (currentUrl.indexOf(REVIEW_URL_PATTERN) !== -1) {
      environment = "review";
    } else if (currentUrl.indexOf(PRODUCTION_URL) !== -1) {
      environment = "production";
    } else {
      throw new TypeError(`Couldn't identify environment for url: ${currentUrl}`);
    }
  }

  return environment;
};
