import Bugsnag from "@bugsnag/expo";
import * as AppAuth from "expo-app-auth";
import * as Google from "expo-google-app-auth";
import * as SecureStore from "expo-secure-store";
import _ from "lodash";
import { Alert, Platform } from "react-native";

import {
  BITBUCKET_LOGIN_KEY_DEV,
  BITBUCKET_LOGIN_KEY_PROD,
  BITBUCKET_LOGIN_SECRET_DEV,
  GOOGLE_LOGIN_KEY_ANDROID_DEV,
  GOOGLE_LOGIN_KEY_ANDROID_PROD,
  GOOGLE_LOGIN_KEY_IOS_DEV,
  GOOGLE_LOGIN_KEY_IOS_PROD,
  MICROSOFT_LOGIN_KEY,
} from "../constants";
import { LOGGER } from "../logger";
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
const getStandardErrorCode: ((code: number) => number) = (
  code: number,
): number => Number(Platform.select({
  android: code,
  default: code,
  ios: (code * -1) - iOSErrorCodeOffset,
}));

/** Normalized user properties */
export interface IUser {
  email: string;
  firstName: string;
  fullName: string;
  id: string;
  lastName?: string;
  photoUrl?: string;
}

/** Auth data provided after login */
export interface IAuthState {
  authProvider: "BITBUCKET" | "GOOGLE" | "MICROSOFT";
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

export const authWithGoogle: (() => Promise<IAuthResult>) = async (
): Promise<IAuthResult> => {
  try {
    const logInResult: Google.LogInResult =
      await Google.logInAsync(googleConfig);

    if (logInResult.type === "success") {
      return {
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
    const errorCode: AppAuthError =
      getStandardErrorCode((error as { code: AppAuthError }).code);

    switch (errorCode) {
      case AppAuthError.UserCanceledAuthorizationFlow:
      case AppAuthError.ProgramCanceledAuthorizationFlow:
        break;
      case AppAuthError.NetworkError:
        Alert.alert(
          i18next.t("common.networkError.title"),
          i18next.t("common.networkError.msg"));
        break;
      default:
        LOGGER.warning(
          "An error occurred authenticating with Google",
          { ...error });
        Alert.alert(
          i18next.t("common.error.title"),
          i18next.t("common.error.msg"));
    }
  }

  return { type: "cancel" };
};

const microsoftConfig: AppAuth.OAuthProps = {
  clientId: MICROSOFT_LOGIN_KEY,
  issuer: "https://sts.windows.net/common/",
  redirectUrl: `${AppAuth.OAuthRedirect}://oauth2redirect/microsoft`,
  scopes: ["openid", "profile", "email"],
  serviceConfiguration: {
    authorizationEndpoint:
      "https://login.microsoftonline.com/common/oauth2/authorize",
    revocationEndpoint:
      "https://login.microsoftonline.com/common/oauth2/logout",
    tokenEndpoint: "https://login.microsoftonline.com/common/oauth2/token",
  },
};

export const authWithMicrosoft: (() => Promise<IAuthResult>) = async (
): Promise<IAuthResult> => {
  try {
    const logInResult: AppAuth.TokenResponse =
      await AppAuth.authAsync(microsoftConfig);
    const userResponse: Response = await fetch(
      "https://login.microsoftonline.com/common/openid/userinfo",
      { headers: { Authorization: `Bearer ${logInResult.accessToken}` } },
    );

    /**
     * User properties returned by Microsoft's Graph API
     * @see https://docs.microsoft.com/en-us/graph/api/resources/user?view=graph-rest-1.0#properties
     */
    const userProps: Record<string, string> =
      await userResponse.json() as Record<string, string>;

    return {
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
    const errorCode: AppAuthError =
      getStandardErrorCode(Number((error as { code: AppAuthError }).code));

    switch (errorCode) {
      case AppAuthError.UserCanceledAuthorizationFlow:
      case AppAuthError.ProgramCanceledAuthorizationFlow:
      case AppAuthError.AccessDenied:
        break;
      default:
        LOGGER.warning(
          "An error occurred authenticating with Microsoft",
          { ...error });
        Alert.alert(
          i18next.t("common.error.title"),
          i18next.t("common.error.msg"));
    }
  }

  return { type: "cancel" };
};

const bitbucketConfig: AppAuth.OAuthProps = {
  clientId: __DEV__ ? BITBUCKET_LOGIN_KEY_DEV : BITBUCKET_LOGIN_KEY_PROD,
  clientSecret:
    __DEV__ ? BITBUCKET_LOGIN_SECRET_DEV : BITBUCKET_LOGIN_SECRET_DEV,
  issuer: "",
  redirectUrl: `${AppAuth.OAuthRedirect}://oauth2redirect/bitbucket`,
  scopes: ["account", "email"],
  serviceConfiguration: {
    authorizationEndpoint: "https://bitbucket.org/site/oauth2/authorize",
    tokenEndpoint: "https://bitbucket.org/site/oauth2/access_token",
  },
};

export const authWithBitbucket: (() => Promise<IAuthResult>) = async (
): Promise<IAuthResult> => {
  try {
    const logInResult: AppAuth.TokenResponse =
      await AppAuth.authAsync(bitbucketConfig);
    const userResponse: Response = await fetch(
      "https://api.bitbucket.org/2.0/user",
      { headers: { Authorization: `Bearer ${logInResult.accessToken}` } },
    );
    const emailsResponse: Response = await fetch(
      "https://api.bitbucket.org/2.0/user/emails",
      { headers: { Authorization: `Bearer ${logInResult.accessToken}` } },
    );

    /**
     * User properties returned by Bitbucket's API
     * @see https://developer.atlassian.com/bitbucket/api/2/reference/resource/user
     */
    interface IUserProps {
      account_id: string;
      display_name: string;
      links: {
        avatar: {
          href: string;
        };
      };
      username: string;
    }
    const userProps: IUserProps = await userResponse.json() as IUserProps;

    /**
     * Accounts may have multiple associated emails but only one primary
     * @see https://developer.atlassian.com/bitbucket/api/2/reference/resource/user/emails
     */
    interface IEmails {
      values: Array<{
        email: string;
        is_primary: boolean;
      }>;
    }
    const { values: emails }: IEmails = await emailsResponse.json() as IEmails;
    const { email: primaryEmail } = emails.find((
      email: IEmails["values"][0]): boolean => email.is_primary,
    ) as IEmails["values"][0];

    return {
      authProvider: "BITBUCKET",
      authToken: logInResult.accessToken as string,
      type: "success",
      user: {
        email: primaryEmail,
        firstName: _.capitalize(userProps.username),
        fullName: _.startCase(userProps.display_name.toLowerCase()),
        id: userProps.account_id,
        photoUrl: userProps.links.avatar.href,
      },
    };
  } catch (error) {
    const errorCode: AppAuthError =
      getStandardErrorCode(Number((error as { code: AppAuthError }).code));

    switch (errorCode) {
      case AppAuthError.UserCanceledAuthorizationFlow:
      case AppAuthError.ProgramCanceledAuthorizationFlow:
      case AppAuthError.AccessDenied:
        break;
      default:
        LOGGER.warning(
          "An error occurred authenticating with Bitbucket",
          { ...error });
        Alert.alert(
          i18next.t("common.error.title"),
          i18next.t("common.error.msg"));
    }
  }

  return { type: "cancel" };
};

export const logout: (() => Promise<void>) = async (): Promise<void> => {
  await SecureStore.deleteItemAsync("integrates_session");
  const authState: string | null = await SecureStore.getItemAsync("authState");
  const { authProvider, authToken }: Record<string, string> = _.isNil(authState)
    ? { authProvider: "", authToken: "" }
    : JSON.parse(authState) as Record<string, string>;

  switch (authProvider) {
    case "BITBUCKET":
      // Bitbucket does not implement a revoke endpoint for oauth2
      break;
    case "GOOGLE":
      Google.logOutAsync({ accessToken: authToken, ...googleConfig })
        .catch((error: Error): void => {
          LOGGER.warning("Couldn't revoke google session", { ...error });
        });
      break;
    case "MICROSOFT":
      AppAuth.revokeAsync(
        microsoftConfig,
        { isClientIdProvided: true, token: authToken })
        .catch((error: Error): void => {
          LOGGER.warning("Couldn't revoke microsoft session", { ...error });
        });
      break;
    default:
  }
  await SecureStore.deleteItemAsync("authState");
  Bugsnag.setUser("", "", "");
};
