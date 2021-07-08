import {
  AuthRequest,
  Prompt,
  ResponseType,
  exchangeCodeAsync,
  fetchDiscoveryAsync,
  makeRedirectUri,
  revokeAsync,
} from "expo-auth-session";
import type {
  AuthSessionResult,
  DiscoveryDocument,
  TokenResponse,
} from "expo-auth-session";
import jwtDecode from "jwt-decode";
import _ from "lodash";

import type { IAuthResult } from "../..";
import { MICROSOFT_CLIENT_ID } from "../../../constants";
import { LOGGER } from "../../../logger";

const clientId: string = MICROSOFT_CLIENT_ID;

const getRedirectUri: () => string = (): string =>
  makeRedirectUri({
    path: "oauth2redirect/microsoft",
    useProxy: false,
  });

const getDiscovery: () => Promise<DiscoveryDocument> =
  async (): Promise<DiscoveryDocument> => {
    const baseDocument: DiscoveryDocument = await fetchDiscoveryAsync(
      "https://login.microsoftonline.com/common/v2.0/"
    );

    return {
      ...baseDocument,
      revocationEndpoint: baseDocument.endSessionEndpoint,
    };
  };

const getTokenResponse: (
  discovery: DiscoveryDocument,
  params: Record<string, string>,
  request: AuthRequest
) => Promise<TokenResponse> = async (
  discovery: DiscoveryDocument,
  params: Record<string, string>,
  request: AuthRequest
): Promise<TokenResponse> =>
  exchangeCodeAsync(
    {
      clientId,
      code: params.code,
      extraParams: {
        code_verifier: request.codeVerifier as string, // eslint-disable-line camelcase -- Defined by API
      },
      redirectUri: getRedirectUri(),
    },
    { tokenEndpoint: discovery.tokenEndpoint }
  );

const authWithMicrosoft: () => Promise<IAuthResult> =
  async (): Promise<IAuthResult> => {
    try {
      const discovery: DiscoveryDocument = await getDiscovery();
      const request: AuthRequest = new AuthRequest({
        clientId,
        prompt: Prompt.SelectAccount,
        redirectUri: getRedirectUri(),
        responseType: ResponseType.Code,
        scopes: ["openid", "profile", "email"],
        usePKCE: true,
      });

      const logInResult: AuthSessionResult = await request.promptAsync(
        discovery,
        { useProxy: false }
      );

      if (logInResult.type === "success") {
        const { idToken } = await getTokenResponse(
          discovery,
          logInResult.params,
          request
        );

        /**
         * User properties
         * @see https://docs.microsoft.com/en-us/azure/active-directory/develop/id-tokens#payload-claims
         */
        const userProps = jwtDecode<Record<string, string>>(idToken as string);

        return {
          authProvider: "MICROSOFT",
          authToken: idToken as string,
          type: "success",
          user: {
            email: _.get(userProps, "email", userProps.upn),
            firstName: _.capitalize(userProps.name.split(" ")[0]),
            fullName: _.startCase(userProps.name.toLowerCase()),
            lastName: userProps.name.split(" ").slice(1).join(" "),
          },
        };
      }
      if (logInResult.type === "error") {
        LOGGER.error("Couldn't authenticate with Microsoft", logInResult);
      }
    } catch (error: unknown) {
      LOGGER.error("Couldn't authenticate with Microsoft", error);
    }

    return { type: "cancel" };
  };

const logoutFromMicrosoft: (authToken: string) => void = async (
  authToken: string
): Promise<void> => {
  try {
    const discovery: DiscoveryDocument = await getDiscovery();

    await revokeAsync(
      { token: authToken },
      { revocationEndpoint: discovery.revocationEndpoint }
    );
  } catch (error: unknown) {
    LOGGER.warning("Couldn't revoke microsoft session", error);
  }
};

export { authWithMicrosoft, logoutFromMicrosoft };
