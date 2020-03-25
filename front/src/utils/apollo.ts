import { InMemoryCache, NormalizedCacheObject } from "apollo-cache-inmemory";
import { ApolloClient } from "apollo-client";
import { ApolloLink, Operation } from "apollo-link";
import { ErrorResponse, onError } from "apollo-link-error";
import { createUploadLink } from "apollo-upload-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import { getEnvironment } from "./context";
import { msgError } from "./notifications";
import translate from "./translations/translate";

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

/**
 * Apollo-compatible wrapper for XHR requests
 *
 * This is a necessary workaround for file upload mutations
 * since the Fetch API that apollo uses by default
 * lacks support for tracking upload progress
 *
 * @see https://github.com/jaydenseric/apollo-upload-client/issues/88
 */
interface IExtendedFetchOptions extends RequestInit {
  notifyUploadProgress: boolean;
  onUploadProgress(ev: ProgressEvent): void;
}

const xhrWrapper: WindowOrWorkerGlobalScope["fetch"] = async (
  uri: string, options: IExtendedFetchOptions,
): Promise<Response> => new Promise((
  resolve: (value: Response) => void,
  reject: (reason: Error) => void,
): void => {
  const xhr: XMLHttpRequest = new XMLHttpRequest();

  xhr.onload = (): void => {
    resolve(new Response(xhr.response, options));
  };

  xhr.onerror = (): void => {
    reject(new Error(`Network request failed: ${xhr.responseText}`));
  };

  xhr.ontimeout = (): void => {
    reject(new Error("Network request timed out"));
  };

  xhr.open(_.get(options, "method", "POST"), uri, true);

  if (options.headers !== undefined) {
    Object.keys(options.headers)
      .forEach((key: string): void => {
        xhr.setRequestHeader(key, _.get(options.headers, key));
      });
  }

  xhr.upload.onprogress = options.onUploadProgress;

  xhr.send(options.body);
});

const extendedFetch: WindowOrWorkerGlobalScope["fetch"] = async (
  uri: string, options: IExtendedFetchOptions,
): Promise<Response> => options.notifyUploadProgress
    ? xhrWrapper(uri, options)
    : fetch(uri, options);

let urlHostApiV1: string;
let urlHostApiV2: string;

const setIntegratesHeaders: Dictionary = {
  "X-CSRFToken": getCookie("csrftoken"),
};

if (window.location.hostname === "localhost") {
    urlHostApiV1 = `${window.location.protocol}//${window.location.hostname}:8080/api`;
    urlHostApiV2 = `${window.location.protocol}//${window.location.hostname}:9090/api`;
    const authHeader: string = "Authorization";
    setIntegratesHeaders[authHeader] = `Bearer ${getCookie("integrates_session")}`;
} else {
    urlHostApiV1 = `${window.location.origin}/integrates/api`;
    urlHostApiV2 = `${window.location.origin}/integrates/v2/api`;
}

const apiLinkV1: ApolloLink = createUploadLink({
  credentials: "same-origin",
  fetch: extendedFetch,
  headers: setIntegratesHeaders,
  uri: urlHostApiV1,
});

const apiLinkV2: ApolloLink = createUploadLink({
  credentials: "same-origin",
  fetch: extendedFetch,
  headers: setIntegratesHeaders,
  uri: urlHostApiV2,
});

export const client: ApolloClient<NormalizedCacheObject> = new ApolloClient({
  cache: new InMemoryCache(),
  connectToDevTools: getEnvironment() !== "production",
  defaultOptions: {
    watchQuery: {
      fetchPolicy: "cache-and-network",
    },
  },
  link: ApolloLink.from([
    // Top-level error handling
    onError(({ graphQLErrors, networkError, response }: ErrorResponse): void => {
      if (networkError !== undefined) {
        const { statusCode } = (networkError as { statusCode: number });

        if (statusCode === 403) {
          // Django CSRF expired
          location.reload();
        }
      } else if (graphQLErrors !== undefined) {
        graphQLErrors.forEach(({ message }: GraphQLError) => {
          if (_.includes(["Login required", "Exception - Invalid Authorization"], message)) {
            if (response !== undefined) {
              response.data = undefined;
              response.errors = [];
            }
            location.assign("/integrates/logout");
          } else if (_.includes(
            ["Access denied", "Exception - Project does not exist", "Exception - Finding not found"],
            message)
          ) {
            if (response !== undefined) {
              response.data = undefined;
              response.errors = [];
            }
            msgError(translate.t("proj_alerts.access_denied"));
          }
        });
      }
    }),
    ApolloLink.split(
        // NOTE: Split GraphQL according to migration status
        (operation: Operation) =>
          ["HomeProjects",
           "GetUserAuthorization",
           "GetAccessTokenQuery",
           "GetUserDataQuery",
           "GetRole",
           "AcceptLegalMutation",
           "InvalidateAccessTokenMutation",
           "UpdateAccessTokenMutation",
           "InternalProjectName",
           "AddUserMutation",
           "GrantUserMutation",
           "RemoveUserAccessMutation",
           "EditUserMutation",
           "UpdateEventDescriptionMutation",
           "SolveEventMutation",
           "CreateEventMutation",
           "UpdateEventEvidenceMutation",
           "DownloadEventFileMutation",
           "RemoveEventEvidenceMutation",
           "GetProjectAlert",
           "GetRepositoriesQuery",
           "GetEnvironmentsQuery",
           "GetFilesQuery",
           "AddEnvironmentsMutation",
           "AddRespositoriesMutation",
           "UploadFileMutation",
           "DownloadFileMutation",
           "RemoveFileMutation",
           "UpdateEnvironmentMutation",
           "UpdateRespositoryMutation",
           "GetForcesExecutions",
           "CreateProjectMutation",
           "RequestRemoveProjectMutation",
           "RejectProjectDeletion",
           "AddTagsMutation",
           "RemoveTagMutation",
           "RemoveEvidenceMutation",
           "UpdateEvidenceMutation",
           "UpdateDescriptionMutation",
           "VerifyFinding",
           "HandleAcceptation",
           "RejectDraftMutation",
           "DeleteFindingMutation",
           "ApproveDraftMutation",
           "CreateDraftMutation",
           "SubmitDraftMutation"].includes(operation.operationName),
        apiLinkV2,
        apiLinkV1,
       ),
  ]),
});
