import { default as ApolloClient } from "apollo-boost";
import _ from "lodash";
import unfetch from "unfetch";

let PRODUCTION_URL: string;
PRODUCTION_URL = "https://fluidattacks.com";

let REVIEW_URL_PATTERN: string;
REVIEW_URL_PATTERN = ".integrates.env";

let DEVELOPMENT_URL: string;
DEVELOPMENT_URL = "https://localhost";

let TESTS_URL: string;
TESTS_URL = "http://localhost/";

const getGrapQLBackend: (() => string) = (): string => {
  let url: string;
  /* tslint:disable-next-line:strict-type-predicates
   * Disabling this rule is necessary because the following expression is
   * misbelived to be always true by the linter while it is necessary for
   * avoiding errors in the npm test environment where the object window
   * doesn't exist.
   */
  if (typeof window === "undefined") {
    url = "https://localhost/integrates/api";
  } else {
    const currentUrl: string = window.location.href;
    if (currentUrl.indexOf(DEVELOPMENT_URL) !== -1 || currentUrl === "about:blank" ||
    currentUrl.indexOf(TESTS_URL) !== -1) {
      url = "https://localhost/integrates/api";
    } else if (currentUrl.indexOf(REVIEW_URL_PATTERN) !== -1) {
      url = "/integrates/api";
    } else if (currentUrl.indexOf(PRODUCTION_URL) !== -1) {
      url = "https://fluidattacks.com/integrates/api";
    } else {
      throw new TypeError(`Couldn't identify environment for url: ${currentUrl}`);
    }
  }

  return url;
};

const getCookie: (name: string) => string = (name: string): string => {
  let cookieValue: string;
  cookieValue = "";
  if (document.cookie !== "") {
    let cookie: string;
    const cookies: string[] = document.cookie.split(";");
    for (cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.substring(0, name.length + 1) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
       }
    }
  }

  return cookieValue;
};

export const showPreloader: () => void = (): void => {
  const preloaderElement: HTMLElement | null = document.getElementById("full_loader");
  if (preloaderElement !== null) {
    preloaderElement.style.display = "block";
  }
};

export const hidePreloader: () => void = (): void => {
  const preloaderElement: HTMLElement | null = document.getElementById("full_loader");
  if (preloaderElement !== null) {
    preloaderElement.style.display = "none";
  }
};

export const client: ApolloClient<{}> = new ApolloClient<{}>({
  credentials: "same-origin",
  fetch: _.isUndefined(fetch) ? unfetch : fetch,
  headers: {
    "X-CSRFToken": getCookie("csrftoken"),
  },
  uri: getGrapQLBackend(),
});
