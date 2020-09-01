import Bugsnag from "@bugsnag/expo";
import * as SecureStore from "expo-secure-store";
import _ from "lodash";

import { LOGGER } from "../logger";

import { logoutFromGoogle } from "./providers/google";
import { logoutFromMicrosoft } from "./providers/microsoft";

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
      logoutFromGoogle(authToken);
      break;
    case "MICROSOFT":
      logoutFromMicrosoft(authToken);
      break;
    default:
      LOGGER.error("Unsupported provider", authProvider);
  }
  await SecureStore.deleteItemAsync("authState");
  Bugsnag.setUser("", "", "");
};

export { authWithGoogle } from "./providers/google";
export { authWithMicrosoft } from "./providers/microsoft";
export { authWithBitbucket } from "./providers/bitbucket";
