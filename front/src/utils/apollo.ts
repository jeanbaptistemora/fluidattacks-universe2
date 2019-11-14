import { InMemoryCache, NormalizedCacheObject } from "apollo-cache-inmemory";
import { ApolloClient } from "apollo-client";
import { ApolloLink } from "apollo-link";
import { createUploadLink } from "apollo-upload-client";
import _ from "lodash";
import { getEnvironment } from "./context";

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

export const client: ApolloClient<NormalizedCacheObject> = new ApolloClient({
  cache: new InMemoryCache(),
  connectToDevTools: getEnvironment() !== "production",
  link: ApolloLink.from([
    createUploadLink({
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      uri: `${window.location.origin}/integrates/api`,
    }),
  ]),
});
