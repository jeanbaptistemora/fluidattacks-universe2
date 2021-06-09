import {
  AuthRequest,
  Prompt,
  ResponseType,
  exchangeCodeAsync,
  fetchDiscoveryAsync,
  fetchUserInfoAsync,
  makeRedirectUri,
  revokeAsync,
} from "expo-auth-session";
import type {
  AuthSessionResult,
  DiscoveryDocument,
  TokenResponse,
} from "expo-auth-session";
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
        const { accessToken } = await getTokenResponse(
          discovery,
          logInResult.params,
          request
        );

        /**
         * User properties returned by Microsoft's Graph API
         * @see https://docs.microsoft.com/en-us/graph/api/resources/user?view=graph-rest-1.0#properties
         */
        const userProps: Record<string, string> = await fetchUserInfoAsync(
          { accessToken },
          { userInfoEndpoint: discovery.userInfoEndpoint }
        );

        return {
          authProvider: "MICROSOFT",
          authToken: accessToken,
          type: "success",
          user: {
            email: _.get(userProps, "upn", userProps.email),
            firstName: _.capitalize(userProps.given_name),
            fullName: _.startCase(userProps.name.toLowerCase()),
            lastName: userProps.family_name,
          },
        };
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
