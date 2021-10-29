import Bugsnag from "@bugsnag/expo";
import { deleteItemAsync, getItemAsync } from "expo-secure-store";
import _ from "lodash";

import { logoutFromGoogle } from "./providers/google";
import { logoutFromMicrosoft } from "./providers/microsoft";

import { LOGGER } from "../logger";

/** Normalized user properties */
interface IUser {
  email: string;
  firstName: string;
  fullName: string;
  lastName?: string;
  photoUrl?: string;
}

/** Auth data provided after login */
interface IAuthState {
  authProvider: "BITBUCKET" | "GOOGLE" | "MICROSOFT";
  authToken: string;
  user: IUser;
}

// Avoid breaking functionality
// eslint-disable-next-line @typescript-eslint/no-type-alias
type IAuthResult = { type: "cancel" } | (IAuthState & { type: "success" });

const logout: (
  setSessionToken: React.Dispatch<React.SetStateAction<string>>
) => Promise<void> = async (
  setSessionToken: React.Dispatch<React.SetStateAction<string>>
): Promise<void> => {
  setSessionToken("");
  await deleteItemAsync("session_token");
  const authState: string | null = await getItemAsync("authState");
  const { authProvider, authToken }: Record<string, string> = _.isNil(authState)
    ? { authProvider: "", authToken: "" }
    : (JSON.parse(authState) as Record<string, string>);

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
  await deleteItemAsync("authState");
  Bugsnag.setUser("", "", "");
};

export { IUser, IAuthState, IAuthResult, logout };
export { authWithGoogle } from "./providers/google";
export { authWithMicrosoft } from "./providers/microsoft";
export { authWithBitbucket } from "./providers/bitbucket";
