import {
  AuthRequest,
  AuthSessionResult,
  DiscoveryDocument,
  exchangeCodeAsync,
  fetchUserInfoAsync,
  makeRedirectUri,
  Prompt,
  resolveDiscoveryAsync,
  ResponseType,
  revokeAsync,
  TokenResponse,
} from "expo-auth-session";
import _ from "lodash";

import { IAuthResult } from "..";
import { MICROSOFT_LOGIN_KEY } from "../../constants";
import { LOGGER } from "../../logger";

const clientId: string = MICROSOFT_LOGIN_KEY;

const getRedirectUri: () => string = (): string =>
  makeRedirectUri({
    path: "oauth2redirect/microsoft",
    useProxy: false,
  });

const getDiscovery: () => Promise<DiscoveryDocument> = async (): Promise<
  DiscoveryDocument
> => {
  const baseDocument: DiscoveryDocument = await resolveDiscoveryAsync(
    "https://login.microsoftonline.com/common",
  );

  return {
    ...baseDocument,
    revocationEndpoint: baseDocument.endSessionEndpoint,
  };
};

const getTokenResponse: (
  discovery: DiscoveryDocument,
  params: Record<string, string>,
  request: AuthRequest,
) => Promise<TokenResponse> = async (
  discovery: DiscoveryDocument,
  params: Record<string, string>,
  request: AuthRequest,
): Promise<TokenResponse> =>
  exchangeCodeAsync(
    {
      clientId,
      code: params.code,
      extraParams: {
        code_verifier: request.codeVerifier as string,
      },
      redirectUri: getRedirectUri(),
    },
    { tokenEndpoint: discovery.tokenEndpoint },
  );

const authWithMicrosoft: () => Promise<IAuthResult> = async (): Promise<
  IAuthResult
> => {
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
      { useProxy: false },
    );

    if (logInResult.type === "success") {
      const { accessToken, idToken } = await getTokenResponse(
        discovery,
        logInResult.params,
        request,
      );

      const userProps: Record<string, string> = await fetchUserInfoAsync(
        { accessToken },
        { userInfoEndpoint: discovery.userInfoEndpoint },
      );

      if (logInResult.type === "success") {
        return {
          authProvider: "MICROSOFT",
          authToken: idToken as string,
          type: "success",
          user: {
            email: _.get(userProps, "upn", userProps.email),
            firstName: _.capitalize(userProps.given_name),
            fullName: _.startCase(userProps.name.toLowerCase()),
            id: "",
            lastName: userProps.family_name,
          },
        };
      }
    }
  } catch (error) {
    LOGGER.error("Couldn't authenticate with Microsoft", { ...error });
  }

  return { type: "cancel" };
};

const logoutFromMicrosoft: (authToken: string) => void = async (
  authToken: string,
): Promise<void> => {
  try {
    const discovery: DiscoveryDocument = await getDiscovery();

    await revokeAsync(
      { token: authToken },
      { revocationEndpoint: discovery.revocationEndpoint },
    );
  } catch (error) {
    LOGGER.warning("Couldn't revoke microsoft session", { ...error });
  }
};

export { authWithMicrosoft, logoutFromMicrosoft };
