import * as AppAuth from "expo-app-auth";
import * as Google from "expo-google-app-auth";
import _ from "lodash";
import { Alert, Platform } from "react-native";

import {
  GOOGLE_LOGIN_KEY_ANDROID_DEV,
  GOOGLE_LOGIN_KEY_ANDROID_PROD,
  GOOGLE_LOGIN_KEY_IOS_DEV,
  GOOGLE_LOGIN_KEY_IOS_PROD,
  MICROSOFT_LOGIN_KEY,
} from "../../utils/constants";
import { rollbar } from "../../utils/rollbar";
import { i18next } from "../../utils/translations/translate";

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
export interface IUser {
  email: string;
  firstName: string;
  fullName: string;
  id: string;
  lastName?: string;
  photoUrl?: string;
}

export type IAuthResult = {
  type: "cancel";
} | {
  authToken: string | null;
  type: "success";
  user: IUser;
};

export const authWithGoogle: (() => Promise<IAuthResult>) = async (): Promise<IAuthResult> => {
  let authResult: IAuthResult = { type: "cancel" };

  try {
    const logInResult: Google.LogInResult = await Google.logInAsync({
      androidClientId: GOOGLE_LOGIN_KEY_ANDROID_DEV,
      androidStandaloneAppClientId: GOOGLE_LOGIN_KEY_ANDROID_PROD,
      iosClientId: GOOGLE_LOGIN_KEY_IOS_DEV,
      iosStandaloneAppClientId: GOOGLE_LOGIN_KEY_IOS_PROD,
      scopes: ["profile", "email"],
    });

    if (logInResult.type === "success") {
      authResult = {
        authToken: logInResult.accessToken,
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

export const authWithMicrosoft: (() => Promise<IAuthResult>) = async (): Promise<IAuthResult> => {
  let authResult: IAuthResult = { type: "cancel" };

  try {
    const logInResult: AppAuth.TokenResponse = await AppAuth.authAsync({
      clientId: MICROSOFT_LOGIN_KEY,
      issuer: "https://login.microsoftonline.com/common/v2.0",
      redirectUrl: `${AppAuth.OAuthRedirect}://oauth2redirect/microsoft`,
      scopes: ["openid", "profile", "email"],
      serviceConfiguration: {
        authorizationEndpoint: "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        tokenEndpoint: "https://login.microsoftonline.com/common/oauth2/v2.0/token",
      },
    });

    const userResponse: Response = await fetch("https://graph.microsoft.com/v1.0/me", {
      headers: { Authorization: `Bearer ${logInResult.accessToken}` },
    });

    /**
     * User properties returned by Microsoft's Graph API
     * @see https://docs.microsoft.com/en-us/graph/api/resources/user?view=graph-rest-1.0#properties
     */
    const userProps: Record<string, string> = await userResponse.json() as Record<string, string>;

    authResult = {
      authToken: logInResult.idToken,
      type: "success",
      user: {
        email: userProps.mail,
        firstName: _.capitalize(userProps.givenName),
        fullName: _.startCase(userProps.displayName?.toLowerCase()),
        id: userProps.id,
        lastName: userProps.surname,
      },
    };
  } catch (error) {
    const errorCode: AppAuthError = getStandardErrorCode((error as { code: AppAuthError }).code);

    switch (errorCode) {
      case AppAuthError.UserCanceledAuthorizationFlow:
      case AppAuthError.ProgramCanceledAuthorizationFlow:
        break;
      default:
        rollbar.error("An error occurred authenticating with Microsoft", error as Error);
        Alert.alert(i18next.t("common.error.title"), i18next.t("common.error.msg"));
    }
  }

  return authResult;
};
