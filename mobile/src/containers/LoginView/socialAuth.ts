import * as Google from "expo-google-app-auth";
import _ from "lodash";
import { Alert, Platform } from "react-native";

import {
  GOOGLE_LOGIN_KEY_ANDROID_DEV,
  GOOGLE_LOGIN_KEY_ANDROID_PROD,
  GOOGLE_LOGIN_KEY_IOS_DEV,
  GOOGLE_LOGIN_KEY_IOS_PROD,
} from "../../utils/constants";
import { rollbar } from "../../utils/rollbar";
import { i18next } from "../../utils/translations/translate";

/**
 * AppAuth Error codes
 * @see https://git.io/JforO for android
 * @see https://git.io/JforG for iOS
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
        break;
      default:
        rollbar.error("An error occurred authenticating with Google", error as Error);
        Alert.alert(i18next.t("common.error.title"), i18next.t("common.error.msg"));
    }
  }

  return authResult;
};
