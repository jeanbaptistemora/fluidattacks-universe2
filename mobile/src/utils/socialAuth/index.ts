import * as AppAuth from "expo-app-auth";
import * as Google from "expo-google-app-auth";
import * as SecureStore from "expo-secure-store";
import _ from "lodash";
import { Alert, Platform } from "react-native";

import {
  GOOGLE_LOGIN_KEY_ANDROID_DEV,
  GOOGLE_LOGIN_KEY_ANDROID_PROD,
  GOOGLE_LOGIN_KEY_IOS_DEV,
  GOOGLE_LOGIN_KEY_IOS_PROD,
  MICROSOFT_LOGIN_KEY,
} from "../constants";
import { rollbar } from "../rollbar";
import { i18next } from "../translations/translate";

/**
 * AppAuth Error codes
 * @see https://git.io/JforO
 */
enum AppAuthError {
  InvalidDiscoveryDocument,
  UserCanceledAuthorizationFlow,
  ProgramCanceledAuthorizationFlow,
  NetworkError,
  ServerError,
  JSONDeserializationError,
  TokenResponseConstructionError,
  AccessDenied = 1002,
}

/**
 * Adjust iOS AppAuth error code offset
 * to match the android AppAuth ones
 * @see https://git.io/JfimI
 */
const iOSErrorCodeOffset: number = 2;
const getStandardErrorCode: ((code: number) => number) = (code: number): number => Platform.select({
  android: code,
  default: code,
  ios: (code * -1) - iOSErrorCodeOffset,
});

/** Normalized user properties */
interface IUser {
  email: string;
  firstName: string;
  fullName: string;
  id: string;
  lastName?: string;
  photoUrl?: string;
}

/** Auth data provided after login */
export interface IAuthState {
  authProvider: "GOOGLE" | "MICROSOFT";
  authToken: string;
  user: IUser;
}

export type IAuthResult = { type: "cancel" } | IAuthState & { type: "success" };

const googleConfig: Google.GoogleLogInConfig = {
  androidClientId: GOOGLE_LOGIN_KEY_ANDROID_DEV,
  androidStandaloneAppClientId: GOOGLE_LOGIN_KEY_ANDROID_PROD,
  iosClientId: GOOGLE_LOGIN_KEY_IOS_DEV,
  iosStandaloneAppClientId: GOOGLE_LOGIN_KEY_IOS_PROD,
  scopes: ["profile", "email"],
};

export const authWithGoogle: (() => Promise<IAuthResult>) = async (): Promise<IAuthResult> => {
  let authResult: IAuthResult = { type: "cancel" };

  try {
    const logInResult: Google.LogInResult = await Google.logInAsync(googleConfig);

    if (logInResult.type === "success") {
      authResult = {
        authProvider: "GOOGLE",
        authToken: logInResult.accessToken as string,
        type: "success",
        user: {
          email: logInResult.user.email as string,
          firstName: _.capitalize(logInResult.user.givenName),
          fullName: _.startCase(logInResult.user.name?.toLowerCase()),
          id: logInResult.user.id as string,
          lastName: logInResult.user.familyName,
          photoUrl: logInResult.user.photoUrl,
        },
      };
    }
  } catch (error) {
    const errorCode: AppAuthError = getStandardErrorCode((error as { code: AppAuthError }).code);

    switch (errorCode) {
      case AppAuthError.UserCanceledAuthorizationFlow:
      case AppAuthError.ProgramCanceledAuthorizationFlow:
        break;
      default:
        rollbar.error("An error occurred authenticating with Google", error as Error);
        Alert.alert(i18next.t("common.error.title"), i18next.t("common.error.msg"));
    }
  }

  return authResult;
};

const microsoftConfig: AppAuth.OAuthProps = {
  clientId: MICROSOFT_LOGIN_KEY,
  issuer: "https://sts.windows.net/common/",
  redirectUrl: `${AppAuth.OAuthRedirect}://oauth2redirect/microsoft`,
  scopes: ["openid", "profile", "email"],
  serviceConfiguration: {
    authorizationEndpoint: "https://login.microsoftonline.com/common/oauth2/authorize",
    revocationEndpoint: "https://login.microsoftonline.com/common/oauth2/logout",
    tokenEndpoint: "https://login.microsoftonline.com/common/oauth2/token",
  },
};

export const authWithMicrosoft: (() => Promise<IAuthResult>) = async (): Promise<IAuthResult> => {
  let authResult: IAuthResult = { type: "cancel" };

  try {
    const logInResult: AppAuth.TokenResponse = await AppAuth.authAsync(microsoftConfig);
    const userResponse: Response = await fetch(
      "https://login.microsoftonline.com/common/openid/userinfo",
      { headers: { Authorization: `Bearer ${logInResult.accessToken}` } },
    );

    /**
     * User properties returned by Microsoft's Graph API
     * @see https://docs.microsoft.com/en-us/graph/api/resources/user?view=graph-rest-1.0#properties
     */
    const userProps: Record<string, string> = await userResponse.json() as Record<string, string>;

    authResult = {
      authProvider: "MICROSOFT",
      authToken: logInResult.idToken as string,
      type: "success",
      user: {
        email: _.get(userProps, "upn", userProps.email),
        firstName: _.capitalize(userProps.given_name),
        fullName: _.startCase(userProps.name.toLowerCase()),
        id: userProps.oid,
        lastName: userProps.family_name,
      },
    };
  } catch (error) {
    const errorCode: AppAuthError = getStandardErrorCode(Number((error as { code: AppAuthError }).code));
    switch (errorCode) {
      case AppAuthError.UserCanceledAuthorizationFlow:
      case AppAuthError.ProgramCanceledAuthorizationFlow:
      case AppAuthError.AccessDenied:
        break;
      default:
        rollbar.error("An error occurred authenticating with Microsoft", error as Error);
        Alert.alert(i18next.t("common.error.title"), i18next.t("common.error.msg"));
    }
  }

  return authResult;
};

export const logout: (() => Promise<void>) = async (): Promise<void> => {
  await SecureStore.deleteItemAsync("integrates_session");
  const authState: string | null = await SecureStore.getItemAsync("authState");
  const { authProvider, authToken }: Record<string, string> = _.isNil(authState)
    ? { authProvider: "", authToken: "" }
    : JSON.parse(authState) as Record<string, string>;

  switch (authProvider) {
    case "GOOGLE":
      Google.logOutAsync({ accessToken: authToken, ...googleConfig })
        .catch((error: Error): void => {
          rollbar.error("Couldn't revoke google session", { ...error });
        });
    case "MICROSOFT":
      AppAuth.revokeAsync(microsoftConfig, { isClientIdProvided: true, token: authToken })
        .catch((error: Error): void => {
          rollbar.error("Couldn't revoke microsoft session", { ...error });
        });
    default:
  }
  await SecureStore.deleteItemAsync("authState");
  rollbar.clearPerson();
};
