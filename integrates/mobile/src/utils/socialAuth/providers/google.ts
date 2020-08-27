import { applicationId } from "expo-application";
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
} from "expo-auth-session";
import { AppOwnership, default as Constants } from "expo-constants";
import _ from "lodash";
import { Platform } from "react-native";

import { IAuthResult } from "..";
import {
  GOOGLE_CLIENT_ID_DEV,
  GOOGLE_LOGIN_KEY_ANDROID_PROD,
  GOOGLE_LOGIN_KEY_IOS_PROD,
} from "../../constants";
import { LOGGER } from "../../logger";

const inExpoClient: boolean = Constants.appOwnership === AppOwnership.Expo;

const clientId: string = inExpoClient
  ? GOOGLE_CLIENT_ID_DEV
  : Platform.select({
      android: GOOGLE_LOGIN_KEY_ANDROID_PROD,
      default: "",
      ios: GOOGLE_LOGIN_KEY_IOS_PROD,
    });

const redirectUri: string = makeRedirectUri({
  native: `${applicationId}:/oauth2redirect/google`,
  path: "oauth2redirect/google",
  useProxy: inExpoClient,
});

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
      redirectUri,
    },
    { tokenEndpoint: discovery.tokenEndpoint },
  );

  return accessToken;
};

const authWithGoogle: () => Promise<IAuthResult> = async (): Promise<
  IAuthResult
> => {
  try {
    const discovery: DiscoveryDocument = await resolveDiscoveryAsync(
      "https://accounts.google.com",
    );
    const request: AuthRequest = new AuthRequest({
      clientId,
      prompt: Prompt.SelectAccount,
      redirectUri,
      responseType: inExpoClient ? ResponseType.Token : ResponseType.Code,
      scopes: [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
      ],
      usePKCE: !inExpoClient,
    });

    await request.makeAuthUrlAsync(discovery);

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
    LOGGER.error("An error occurred authenticating with Google", { ...error });
  }

  return { type: "cancel" };
};

export { authWithGoogle };
