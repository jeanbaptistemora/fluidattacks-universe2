import { GoogleUser } from "expo-google-app-auth";
import { RouteComponentProps } from "react-router-native";

export type IWelcomeProps = RouteComponentProps<{}, {}, {
  authProvider: string;
  authToken: string;
  pushToken: string;
  userInfo: GoogleUser;
}>;

/**
 * Sign in response type
 */
export interface ISignInResult {
  signIn: {
    authorized: boolean;
    sessionJwt: string;
    success: boolean;
  };
}
