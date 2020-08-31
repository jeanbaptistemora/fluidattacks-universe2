import {
  AuthRequest,
  AuthSessionResult,
  DiscoveryDocument,
  exchangeCodeAsync,
  fetchDiscoveryAsync,
  fetchUserInfoAsync,
  makeRedirectUri,
  Prompt,
  ResponseType,
  revokeAsync,
} from "expo-auth-session";
import { AppOwnership, default as Constants } from "expo-constants";
import _ from "lodash";
import { Platform } from "react-native";

import { IAuthResult } from "..";
import {
  GOOGLE_CLIENT_ID_ANDROID,
  GOOGLE_CLIENT_ID_DEV,
  GOOGLE_CLIENT_ID_IOS,
} from "../../constants";
import { LOGGER } from "../../logger";

const inExpoClient: boolean = Constants.appOwnership === AppOwnership.Expo;

const clientId: string = inExpoClient
  ? GOOGLE_CLIENT_ID_DEV
  : Platform.select({
      android: GOOGLE_CLIENT_ID_ANDROID,
      default: "",
      ios: GOOGLE_CLIENT_ID_IOS,
    });

const getRedirectUri: () => string = (): string => makeRedirectUri({
  path: "oauth2redirect/google",
  useProxy: inExpoClient,
});

const getDiscovery: () => Promise<DiscoveryDocument> = async (): Promise<
  DiscoveryDocument
> => fetchDiscoveryAsync("https://accounts.google.com");

const getAccessToken: (
  discovery: DiscoveryDocument,
  params: Record<string, string>,
  request: AuthRequest,
) => Promise<string> = async (
  discovery: DiscoveryDocument,
  params: Record<string, string>,
  request: AuthRequest,
): Promise<string> => {
  if (inExpoClient) {
    return params.access_token;
  }

  const { accessToken } = await exchangeCodeAsync(
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

  return accessToken;
};

const authWithGoogle: () => Promise<IAuthResult> = async (): Promise<
  IAuthResult
> => {
  try {
    const discovery: DiscoveryDocument = await getDiscovery();
    const request: AuthRequest = new AuthRequest({
      clientId,
      prompt: Prompt.SelectAccount,
      redirectUri: getRedirectUri(),
      responseType: inExpoClient ? ResponseType.Token : ResponseType.Code,
      scopes: [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
      ],
      usePKCE: !inExpoClient,
    });

    const logInResult: AuthSessionResult = await request.promptAsync(
      discovery,
      { useProxy: inExpoClient },
    );

    if (logInResult.type === "success") {
      const accessToken: string = await getAccessToken(
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
          authProvider: "GOOGLE",
          authToken: accessToken,
          type: "success",
          user: {
            email: userProps.email,
            firstName: _.capitalize(userProps.given_name),
            fullName: _.startCase(userProps.name.toLowerCase()),
            id: "",
            lastName: userProps.familyName,
            photoUrl: userProps.picture,
          },
        };
      }
    }
  } catch (error) {
    LOGGER.error("Couldn't authenticate with Google", { ...error });
  }

  return { type: "cancel" };
};

const logoutFromGoogle: (authToken: string) => void = async (
  authToken: string,
): Promise<void> => {
  try {
    const discovery: DiscoveryDocument = await getDiscovery();

    await revokeAsync(
      { token: authToken },
      { revocationEndpoint: discovery.revocationEndpoint },
    );
  } catch (error) {
    LOGGER.warning("Couldn't revoke google session", { ...error });
  }
};

export { authWithGoogle, logoutFromGoogle };
