import Axios, { AxiosPromise, AxiosRequestConfig } from "axios";
import rollbar from "../utils/rollbar";
import { getEnvironment } from "./context";

/**
 * XHR request wrapper
 * for backend communication using GraphQL queries
 */
class Xhr {

  public constructor() {
    this.axiosConfig();
  }

  /**
   * Add the CSRF cookie to all requests.
   * function axiosConfig
   * return {undefined}
   */
  public axiosConfig = (): void => {
    const csrftoken: string = this.getCookie("csrftoken");
    Axios.interceptors.request.use((config: AxiosRequestConfig) => {
      if (!this.csrfSafeMethod(config.method as string) && this.sameOrigin(config.url as string)) {
        config.headers = {
          "X-CSRFToken": csrftoken,
        };
      }

      return config;
    });
  }

  /**
   * Verify the send method of cookie request.
   * function csrfSafeMethod
   * param {String} method Request method for get cookies
   * return {boolean} Return boolean if request method is valid
   */
  public csrfSafeMethod = (method: string): boolean =>
       new RegExp("/^(GET|HEAD|OPTIONS)$/").test(method)

  /**
   * Get cookies by name.
   * function getCookie
   * param {string} name Cookie name
   * return {null|string} Return the cookies of a previous session
   */
  public getCookie = (name: string): string => {
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
   }

 /**
  * Hide preloader animation
  * function hidePreloader
  * return {void}
  */
  public hidePreloader = (): void => {
     const preloaderElement: HTMLElement =
        document.getElementById("full_loader") as HTMLElement;
     preloaderElement.style.display = "none";
   }

  /**
   * Perform axios (ajax) request against GraphQL endpoint
   */
  public request = (query: string, errorText: string): AxiosPromise<void> => {
    this.showPreloader();
    const promise: AxiosPromise<void> =
      Axios.post<void>(
        getEnvironment() === "production"
        ? "integrates/api"
        : "api",
        query,
      );
    // tslint:disable-next-line:no-floating-promises
    promise.then(() => {
      this.hidePreloader();
    });
    promise.catch(() => {
      this.hidePreloader();
      rollbar.error(errorText);
    });

    return promise;
  }

  /**
   * Verify if the url is in Integrates domain.
   * function sameOrigin
   * param {string} url Current user url
   * return {boolean} Boolean response if the provided url is valid
   */
  public sameOrigin = (url: string): boolean => {
    const hostOrigin: string = document.location.host;
    const protocolOrigin: string = document.location.protocol;
    let srOrigin: string;
    srOrigin = `//${hostOrigin}`;
    const origin: string = protocolOrigin + srOrigin;

    return url === origin || url.slice(0, origin.length + 1) === `${origin}/` ||
          (url === srOrigin || url.slice(0, srOrigin.length + 1) ===
          `${srOrigin}/`) || !(/^(\/\/|http:|https:).*/).test(url);
  }

  /**
   * Show preloader animation
   * function showPreloader
   * return {void}
   */
  public showPreloader = (): void => {
    const preloaderElement: HTMLElement =
        document.getElementById("full_loader") as HTMLElement;
    preloaderElement.style.display = "block";
  }
}

export = Xhr;
