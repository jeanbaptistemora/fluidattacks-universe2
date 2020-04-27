import { RouteComponentProps } from "react-router-native";

import { ILoginState } from "../LoginView/reducer";

export type IWelcomeProps = RouteComponentProps<{}, {}, {
  authProvider: string;
  authToken: string;
  pushToken: string;
  userInfo: ILoginState["userInfo"];
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
