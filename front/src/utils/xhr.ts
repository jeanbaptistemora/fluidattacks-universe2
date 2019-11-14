import Axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from "axios";
import _ from "lodash";
import { msgError } from "./notifications";
import translate from "./translations/translate";

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
     const preloaderElement: HTMLElement | null = document.getElementById("full_loader");
     if (preloaderElement !== null) {
       preloaderElement.style.display = "none";
     }
   }

  /**
   * Perform axios (ajax) request against GraphQL endpoint
   */
   /* tslint:disable:no-any
    * Disabling here is necessary becase this is a generic function that will
    * return promises with objects of different types as response
   */
  public request = async (query: string, errorText: string): Promise<any> => {
    const payload: { query: string } = {query};

    return this.executeRequest(payload, errorText);
  }
  // tslint:enable:no-any

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
    const preloaderElement: HTMLElement | null = document.getElementById("full_loader");
    if (preloaderElement !== null) {
      preloaderElement.style.display = "block";
    }
  }

  /**
   * Upload files with GraphQL queries
   */
   /* tslint:disable:no-any
    * Disabling here is necessary becase this is a generic function that will
    * return promises with objects of different types as response
   */
  public upload = async (
    query: string, fieldId: string, errorText: string, callbackFn?: ((progress: number) => void)): Promise<any> => {
    const selected: FileList | null = (document.querySelector(fieldId) as HTMLInputElement).files;
    if (_.isNil(selected) || selected.length === 0) {
      msgError(translate.t("proj_alerts.no_file_selected"));
      throw new Error();
    } else {
      const payload: FormData = new FormData();
      // tslint:disable-next-line: no-null-keyword
      payload.append("operations", JSON.stringify({query, variables: {file: null}}));
      payload.append("map", JSON.stringify({1: ["variables.file"]}));
      payload.append("1", selected[0]);

      return this.executeRequest(payload, errorText, callbackFn);
    }
  }

  // tslint:enable:no-any

  /**
   * Perform a POST request against the GraphQL endpoint.
   * function executeRequest
   * param payload {FormData} request content
   * param errorText {string} message to report if request fails
   * return {Promise<any>} generic request promise
   */
   /* tslint:disable:no-any
    * Disabling here is necessary becase this is a generic function that will
    * return promises with objects of different types as response
   */

  private readonly executeRequest:
  ((arg1: {}, arg2: string, callbackFn?: ((progress: number) => void)) => Promise<any>) =
    async (payload: {}, errorText: string, callbackFn?: ((progress: number) => void)) => {
    this.showPreloader();

    const config: AxiosRequestConfig = {
      onUploadProgress: (progressEvent: {loaded: number; total: number}): void => {
          const percentCompleted: number = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          if (callbackFn !== undefined) { callbackFn(percentCompleted); }
        },
    };

    const promise: Promise<any> = Axios.post(
    `${window.location.origin}/integrates/api`,
    payload,
    config,
    )
    .then((response: AxiosResponse) => {
      this.hidePreloader();
      const { data, errors } = response.data;
      if (_.isNil(data)) {
        location.reload();
      } else {
        if (errors) {
         this.hidePreloader();
         const { message } = errors[0];

         if (_.includes(["Login required", "Exception - Invalid Authorization"], message)) {
            location.assign("/integrates/logout");
          } else if (message === "Access denied") {
            msgError(translate.t("proj_alerts.access_denied"));
          } else {
            const exception: AxiosError = {
             config: response.config,
             isAxiosError: true,
             message: errorText,
             name: "AxiosError",
             response,
            };
            throw exception;
          }

         throw new Error();
        } else {

          return response;
        }
      }
    });

    return promise;
  }
}

export = Xhr;
